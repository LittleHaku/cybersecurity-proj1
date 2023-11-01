from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Quiz
from quizzapp.models import CustomUser
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomAuthenticationForm


# Create your views here.


# Register View
def RegisterView(request):
    print("RegisterView")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


# Login View
def LoginView(request):
    print("LoginView")
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form})


# Logout View
@login_required
def LogoutView(request):
    logout(request)
    return redirect("login")


# List all the quizzes
def QuizListView(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz_list.html", {"quizzes": quizzes})


# Detail Quiz, shows the name, the number of questions and a button to start the quiz
def QuizDetailView(request, pk):
    quiz = Quiz.objects.get(id=pk)
    return render(request, "quiz_detail.html", {"quiz": quiz})
