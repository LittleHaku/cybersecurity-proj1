"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quizzapp.views import (
    QuizListView,
    LoginView,
    RegisterView,
    LogoutView,
    MyQuizListView,
    QuizCreateView,
    QuizDeleteView,
    QuizDetailView,
    QuizEditView,
    QuestionEditView,
    QuestionCreateView,
    QuestionDeleteView,
    AnswerCreateView,
    AnswerDeleteView,
    AnswerEditView,
    QuizPlayView,
    IncorrectView,
    YouWonView,
    CheatingView,
    CSRFDemoView,
    FakePasswordsApiView,
    FakeDetailsApiView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", QuizListView, name="home"),
    path("login/", LoginView, name="login"),
    path("register/", RegisterView, name="register"),
    path("logout/", LogoutView, name="logout"),
]

# Quiz
urlpatterns += [
    path("myquizzes/", MyQuizListView, name="myquizzes"),
    path("quiz/create/", QuizCreateView, name="quiz_create"),
    path("quiz/<int:pk>/delete/", QuizDeleteView, name="quiz_delete"),
    path("quiz/<int:pk>/", QuizDetailView, name="quiz_detail"),
    path("quiz/<int:pk>/edit/", QuizEditView, name="quiz_edit"),
]

# Question
urlpatterns += [
    path("question/<int:pk>/edit/", QuestionEditView, name="question_edit"),
    path(
        "question/create/<int:quiz_id>",
        QuestionCreateView,
        name="question_add",
    ),
    path(
        "question/<int:pk>/delete/", QuestionDeleteView, name="question_delete"
    ),
]

# Answer
urlpatterns += [
    path("answer/<int:pk>/edit/", AnswerEditView, name="answer_edit"),
    path(
        "answer/create/<int:question_id>", AnswerCreateView, name="answer_add"
    ),
    path("answer/<int:pk>/delete/", AnswerDeleteView, name="answer_delete"),
]


# Play
urlpatterns += [
    path("play/<int:pk>/", QuizPlayView, name="quiz_play"),
    path("incorrect/", IncorrectView, name="incorrect"),
    path("youwon/", YouWonView, name="you_won"),
    path("cheating/", CheatingView, name="cheating")
]

# CSRF

urlpatterns += [
    path("csrf/", CSRFDemoView, name="csrf_demo")
]

# FAKE API

urlpatterns += [
    path('passwords/', FakePasswordsApiView.as_view(), name='fake_api'),
    path('details/<int:pk>', FakeDetailsApiView.as_view(), name='fake_details_api')
]
