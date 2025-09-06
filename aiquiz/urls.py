from django.urls import path
from . import views

urlpatterns = [
    path("ai-quiz/<str:language>/<str:level>/", views.ai_quiz, name="ai_quiz"),
]
