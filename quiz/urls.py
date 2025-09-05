from django.urls import path 
from . import views
urlpatterns = [
    path("",views.create_quiz,name="quiz"),
    path("quiz/", views.take_quiz, name="take_quiz"),                # no language → ask to select
    path("quiz/<str:language>/", views.take_quiz, name="take_quiz"),
    path("quiz-history/", views.quiz_with_history, name="quiz_with_history"),
]
