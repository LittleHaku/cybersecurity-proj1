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
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", QuizListView, name="home"),
    path("quiz/<int:pk>/", QuizListView, name="quiz"),
    path("login/", LoginView, name="login"),
    path("register/", RegisterView, name="register"),
    path("logout/", LogoutView, name="logout"),
    path("myquizzes/", MyQuizListView, name="myquizzes"),
    path("quiz/create/", QuizCreateView, name="quiz_create"),
    path("quiz/<int:pk>/delete/", QuizDeleteView, name="quiz_delete"),
    path("quiz/<int:pk>/", QuizDetailView, name="quiz_detail"),
]
