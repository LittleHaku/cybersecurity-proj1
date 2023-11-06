from urllib.parse import urlparse
import re
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

from quizzapp.forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    QuizForm,
    AnswerForm,
    QuestionForm,
)
from quizzapp.models import CustomUser, Quiz, Question, Answer
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
# @login_required
def QuizDeleteView(request, pk):
    quiz = Quiz.objects.get(id=pk)
    # if request.user == quiz.owner:
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
    url = request.GET.get('url')

    pattern = re.compile(r'^/details/\d+$')

    # no details are going to be fetched, it is just to show the SSRF vulnerability
    if url:
        parsed_url = urlparse(url)
        """ if pattern.match(parsed_url.path): """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                quiz_details = response.text
                return render(request, 'quiz_detail.html', {'quiz': quiz, 'details': quiz_details})
            else:
                pass
        except requests.exceptions.RequestException as e:
            print(e)
            pass
        """ else:
            return redirect('cheating') """

    request.session["lost"] = False
    request.session["quiz_id"] = pk
    return render(request, "quiz_detail.html", {"quiz": quiz})
# Edit Quiz View


@login_required
def QuizEditView(request, pk):
    quiz = Quiz.objects.get(id=pk)
    if request.user == quiz.owner:
        if request.method == "POST":
            form = QuizForm(request.POST, instance=quiz)
            if form.is_valid():
                new_title = request.POST.get('title')
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE quizzapp_quiz SET title = '{new_title}' WHERE id = {pk}")
                return redirect("quiz_edit", pk=quiz.id)
                """ form.save()
                return redirect("quiz_edit", pk=quiz.id) """
        else:
            form = QuizForm(instance=quiz)
        questions = quiz.question_set.all()
        owner_name = quiz.owner.username
        answers = {}
        for question in questions:
            answers[question.id] = question.answer_set.all()
        return render(
            request,
            "quiz_edit.html",
            {
                "form": form,
                "quiz": quiz,
                "questions": questions,
                "owner_name": owner_name,
                "answers": answers,
            },
        )
    else:
        return redirect("home")


#### QUESTION ####


# Edit Question View
@login_required
def QuestionEditView(request, pk):
    question = Question.objects.get(id=pk)
    quiz = question.quiz
    if request.user == question.quiz.owner:
        answers = question.answer_set.all()
        if request.method == "POST":
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect("question_edit", pk=question.id)
        else:
            form = QuestionForm(instance=question)
        return render(
            request,
            "question_edit.html",
            {
                "form": form,
                "question": question,
                "answers": answers,
                "quiz": quiz,
            },
        )
    else:
        return redirect("home")


# Add Question View
@login_required
@csrf_exempt
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
        question = answer.question
        answer.delete()

        return redirect("question_edit", pk=question.id)

    else:
        return redirect("home")


# Edit Answer View
@login_required
def AnswerEditView(request, pk):
    answer = Answer.objects.get(id=pk)
    question = answer.question

    if request.user == answer.question.quiz.owner:
        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.owner = request.user
            answer.save()

        return redirect("question_edit", pk=question.id)
    else:
        return redirect("home")


#### PLAY ####


# Play Quiz View
def QuizPlayView(request, pk):

    if request.session["lost"]:
        return redirect("cheating")

    if request.session["quiz_id"] != pk:
        return redirect("cheating")

    quiz = Quiz.objects.get(id=pk)
    questions = quiz.question_set.all()

    if "question_id" in request.POST:
        question = Question.objects.get(id=request.POST["question_id"])
        selected_answer = Answer.objects.get(id=request.POST["answer_id"])

        if selected_answer.is_correct:
            # Move to the next question or end the quiz if it was the last question
            next_question = questions.filter(id__gt=question.id).first()
            if next_question:
                return render(
                    request, "quiz_play.html", {"question": next_question}
                )
            else:
                return redirect("you_won")
        else:
            return redirect("incorrect")
    else:
        # This is the first question
        first_question = questions.first()
        return render(request, "quiz_play.html", {"question": first_question})


def CheatingView(request):
    return render(request, "cheating.html")


def YouWonView(request):
    return render(request, "you_won.html")


def IncorrectView(request):
    request.session["lost"] = True
    return render(request, "incorrect.html")

#### CSRF DEMO ####


@login_required
def CSRFDemoView(request):
    quizzes = Quiz.objects.filter(owner=request.user)
    quiz_id = quizzes.first().id if quizzes.exists() else None
    quiz_name = quizzes.first().title if quizzes.exists() else None
    return render(request, "csrf_demo.html", {"quiz_id": quiz_id, "quiz_name": quiz_name})


#### FAKE API ####


class FakePasswordsApiView(APIView):

    def get(self, request):

        data = {
            "user1": "password1",
            "user2": "password2"
        }
        return JsonResponse(data)


class FakeDetailsApiView(APIView):

    def get(self, request, pk):

        topics = {
            1: "common knowledge",
            2: "history",
            3: "science"
        }

        data = {
            "topic": topics.get(int(pk), "not found"),
        }
        return JsonResponse(data)
