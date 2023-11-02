from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quizzapp.models import Quiz, Question, Answer


def create_users():
    User = get_user_model()

    # Create two users
    user1 = User.objects.create_user(
        username='user1', password='password1')
    user2 = User.objects.create_user(
        username='user2', password='password2')

    return user1, user2


def create_quizzes(user1, user2):
    # Create two quizzes
    quiz1 = Quiz.objects.create(title='Quiz 1', owner=user1)
    quiz2 = Quiz.objects.create(title='Quiz 2', owner=user2)

    return quiz1, quiz2


def create_question(quiz, text, answers):
    # Create question
    question = Question.objects.create(quiz=quiz, text=text)

    # Create answers for question
    for answer in answers:
        Answer.objects.create(
            question=question, text=answer['text'], is_correct=answer['is_correct'])

    return question


class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        user1, user2 = create_users()
        quiz1, quiz2 = create_quizzes(user1, user2)

        # Create questions for both quizzes
        create_question(
            quiz1,
            'What is the capital of Spain?',
            [
                {'text': 'Paris', 'is_correct': False},
                {'text': 'Madrid', 'is_correct': True},
                {'text': 'Berlin', 'is_correct': False},
                {'text': 'Rome', 'is_correct': False},
            ]
        )

        create_question(
            quiz1,
            'How many championships has the driver Fernando Alonso won?',
            [
                {'text': '1', 'is_correct': False},
                {'text': '2', 'is_correct': True},
                {'text': '3', 'is_correct': False},
                {'text': '4', 'is_correct': False},
            ]
        )

        create_question(
            quiz1,
            'Who wrote the novel "1984"?',
            [
                {'text': 'George Orwell', 'is_correct': True},
                {'text': 'Aldous Huxley', 'is_correct': False},
                {'text': 'Ray Bradbury', 'is_correct': False},
                {'text': 'Ernest Hemingway', 'is_correct': False},
            ]
        )

        create_question(
            quiz1,
            'What is the capital of Australia?',
            [
                {'text': 'Sydney', 'is_correct': False},
                {'text': 'Melbourne', 'is_correct': False},
                {'text': 'Brisbane', 'is_correct': False},
                {'text': 'Canberra', 'is_correct': True},
            ]
        )

        create_question(
            quiz2,
            'Who directed the movie "Inception"?',
            [
                {'text': 'Christopher Nolan', 'is_correct': True},
                {'text': 'Steven Spielberg', 'is_correct': False},
                {'text': 'Quentin Tarantino', 'is_correct': False},
                {'text': 'Martin Scorsese', 'is_correct': False},
            ]
        )

        create_question(
            quiz2,
            'Who played Tony Stark in the Marvel Cinematic Universe?',
            [
                {'text': 'Chris Evans', 'is_correct': False},
                {'text': 'Robert Downey Jr.', 'is_correct': True},
                {'text': 'Chris Hemsworth', 'is_correct': False},
                {'text': 'Mark Ruffalo', 'is_correct': False},
            ]
        )

        create_question(
            quiz2,
            'What is the largest country in the world?',
            [
                {'text': 'China', 'is_correct': False},
                {'text': 'USA', 'is_correct': False},
                {'text': 'Russia', 'is_correct': True},
                {'text': 'Canada', 'is_correct': False},
            ]
        )

        create_question(
            quiz2,
            'What is the racing number of Lightning McQueen?',
            [
                {'text': '55', 'is_correct': False},
                {'text': '69', 'is_correct': False},
                {'text': '1', 'is_correct': False},
                {'text': '95', 'is_correct': True},
            ]
        )
