from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models

class Quiz(models.Model):
    LANGUAGE_OPTIONS = [
        ('PYTHON', 'Python'),
        ('JAVASCRIPT', 'JavaScript'),
        ('C','C')
    ]

    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_OPTIONS,
        default='PYTHON'
    )
    questions = models.JSONField()
    def __str__(self):
        return self.language
#! example      
# {
#   "What is Python?": [
#     ["Language", "Some explanation about it", true],
#     ["Snake", "Reptile found in jungles", false],
#     ["Car", "A vehicle", false],
#     ["Fruit", "Edible item", false]
#   ],
#   "Second question?": [
#     ["Option1", "Explanation1", false],
#     ["Option2", "Explanation2", true],
#     ["Option3", "Explanation3", false],
#     ["Option4", "Explanation4", false]
#   ]
# }


class QuizHistory(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    score = models.IntegerField(_("Score"))
    date_taken = models.DateTimeField(_("Date Taken"), auto_now_add=True)
    detail=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} - {self.score} on {self.date_taken}"
