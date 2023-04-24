from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.forms import CustomUserCreationForm


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('storage:current_storage')
        else:
            context = {'error': 'Invalid credentials'}
            return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('storage:current_storage')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def profile_view(request):
    user = request.user
    context = {'user': user}
    return render(request, 'storage/profile.html', context)
