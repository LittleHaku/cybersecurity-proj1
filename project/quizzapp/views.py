from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Quiz, Question, Answer
from quizzapp.models import CustomUser
from django.contrib.auth import get_user_model
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    QuizForm,
    AnswerForm,
    QuestionForm,
)


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


#### QUIZ ####


# Quiz delete
@login_required
def QuizDeleteView(request, pk):
    quiz = Quiz.objects.get(id=pk)
    if request.user == quiz.owner:
        quiz.delete()
    return redirect("myquizzes")


# Quiz create
@login_required
def QuizCreateView(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.owner = request.user
            quiz.save()
            return redirect("myquizzes")
    else:
        form = QuizForm()
    return render(request, "quiz_create.html", {"form": form})


# List MY quizzes
@login_required
def MyQuizListView(request):
    quizzes = Quiz.objects.filter(owner=request.user)
    return render(request, "myquiz_list.html", {"quizzes": quizzes})


# List all the quizzes
def QuizListView(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz_list.html", {"quizzes": quizzes})


# Detail Quiz, shows the name, the number of questions and a button to start the quiz
def QuizDetailView(request, pk):
    quiz = Quiz.objects.get(id=pk)
    return render(request, "quiz_detail.html", {"quiz": quiz})


# Quiz Owner view, lets the owner modify the quiz
@login_required
def QuizEditView(request, pk):
    quiz = Quiz.objects.get(id=pk)
    if request.user == quiz.owner:
        questions = quiz.question_set.all()
        owner_name = quiz.owner.username
        return render(
            request,
            "quiz_edit.html",
            {"quiz": quiz, "questions": questions, "owner_name": owner_name},
        )
    else:
        return redirect("home")


#### QUESTION ####


# Edit Question View
@login_required
def QuestionEditView(request, pk):
    question = Question.objects.get(id=pk)
    if request.user == question.quiz.owner:
        answers = question.answer_set.all()
        if request.method == "POST":
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect("quizowner", pk=question.quiz.id)
        else:
            form = QuestionForm(instance=question)
        return render(
            request,
            "question_edit.html",
            {"form": form, "question": question, "answers": answers},
        )
    else:
        return redirect("home")


# Add Question View
@login_required
def QuestionCreateView(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.user == quiz.owner:
        form = QuestionForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()
                return redirect("quiz_edit", pk=quiz.id)
        return render(request, "question_add.html", {"form": form})
    else:
        return redirect("home")


# Delete Question View
@login_required
def QuestionDeleteView(request, pk):
    question = Question.objects.get(id=pk)
    if request.user == question.quiz.owner:
        question.delete()
        return redirect("quiz_edit", pk=question.quiz.id)
    else:
        return redirect("home")


#### ANSWER ####


# Create Answer View
@login_required
def AnswerCreateView(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.owner = request.user
            answer.question = question
            answer.save()
            return redirect("question_edit", pk=question_id)
    else:
        form = AnswerForm()
    return render(request, "answer_add.html", {"form": form})


# Delete Answer View
@login_required
def AnswerDeleteView(request, pk):
    answer = Answer.objects.get(id=pk)
    if request.user == answer.question.quiz.owner:
        answer.delete()
        return redirect("question_edit", pk=answer.question.id)
    else:
        return redirect("home")
