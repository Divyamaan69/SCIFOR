from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.start_quiz, name='start_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('history/', views.history, name='history'),
]
