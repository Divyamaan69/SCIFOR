from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render, redirect
from .models import QuizHistory

def start_quiz(request):
    response = requests.get('https://opentdb.com/api.php?amount=10&type=multiple')
    questions = response.json().get('results', [])
    request.session['questions'] = questions
    return render(request, 'quiz.html', {'questions': questions})


def submit_quiz(request):
    questions = request.session.get('questions', [])
    score = 0
    for i, question in enumerate(questions):
        correct_answer = question['correct_answer'].strip().lower()
        user_answer = request.POST.get(f'question-{i}', '').strip().lower()
        if user_answer == correct_answer:
            score += 1

    if request.user.is_authenticated:
        QuizHistory.objects.create(user=request.user, score=score)

    return render(request, 'result.html', {'score': score})

from django.shortcuts import render
from .models import QuizHistory

def history(request):
    if request.user.is_authenticated:
        history = QuizHistory.objects.filter(user=request.user)
    else:
        history = QuizHistory.objects.filter(session_id=request.session.session_key)

    return render(request, 'history.html', {'history': history})

from django.utils.timezone import now

def save_quiz_history(request, quiz_data):
    user = request.user if request.user.is_authenticated else None
    session_id = request.session.session_key if not user else None

    quiz_history = QuizHistory.objects.create(
        user=user,
        session_id=session_id,
        quiz_data=quiz_data,
        date_taken=now()
    )
