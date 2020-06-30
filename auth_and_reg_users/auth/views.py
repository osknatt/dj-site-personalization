from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(
        request,
        'home.html'

    )


def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            return redirect('/login/')
    else:
        user_form = UserCreationForm()
    return render(request,
                  'signup.html',
                  {'user_form': user_form})


