import random
from django.shortcuts import render, redirect
from .models import Player, Game
from .forms import NumberForm


def clear(request):
    # request.session.pop('player_id', None)
    request.session.pop('game_id', None)
    return redirect('/')


def show_home(request):
    player_id = request.session.get('player_id')
    game_id = request.session.get('game_id')
    print(player_id)
    print(game_id)

    if not player_id:
        player_id = request.session.session_key
        request.session['player_id'] = player_id
        player = Player(id=player_id)
        player.save()
    else:
        player = Player.objects.get(id=player_id)

    player_id = request.session.get('player_id')
    game_id = request.session.get('game_id')
    print(player_id)
    print(game_id)

    if not game_id:
        try:
            game = Game.objects.get(guest=None, is_finished=False)
        except Game.DoesNotExist:
            game = None

        if game:
            game.guest = player
        else:
            game = Game(author=player, number=random.randint(1, 100))
        game.save()
        game_id = game.id
        request.session['game_id'] = game_id
    else:
        game = Game.objects.get(id=game_id)
        if game.is_finished:
            del request.session['game_id']
            return redirect('/')

    player_id = request.session.get('player_id')
    game_id = request.session.get('game_id')
    print(player_id)
    print(game_id)

    context = {}

    if request.method == "POST":
        form = NumberForm(data=request.POST)
        if form.is_valid():
            number = int(request.POST.get('number'))
            game.steps_before_win += 1
            if number == game.number:
                game.is_finished = True
                del request.session['game_id']
                context['message'] = f'Number is guessed by {game.steps_before_win} steps.'
            else:
                if number > game.number:
                    context['message'] = 'Your number is greater than needed'
                else:
                    context['message'] = 'Your number is less than needed'
            game.save()
        context['form'] = form
    else:
        context['form'] = NumberForm()

    context['game'] = game

    return render(request, 'home.html', context)
