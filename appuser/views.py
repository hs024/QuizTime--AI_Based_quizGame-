from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def Home(request):
    return render(request, 'Home.html')

def UserRegister(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # create_user already hashes password
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()
        return redirect('login')   # better UX: go to login after register

    return render(request, 'Register.html')

def UserLogin(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')   # use url name, not render redirect to template
        else:
            return render(request, 'Login.html', {'error': 'Invalid credentials'})

    return render(request, 'Login.html')

def UserLogout(request):
    logout(request)   # you must pass request
    return redirect('home')
