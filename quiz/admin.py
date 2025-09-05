from django.contrib import admin
from .models import Quiz, QuizHistory
import json
from django.utils.safestring import mark_safe

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "language", "preview_questions")
    search_fields = ("language",)

    def preview_questions(self, obj):
        try:
            data = json.dumps(obj.questions, indent=2)
            return mark_safe(f"<pre>{data}</pre>")
        except Exception:
            return obj.questions
    preview_questions.short_description = "Questions"


@admin.register(QuizHistory)
class QuizHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "date_taken", "detail")
    search_fields = ("user__username", "detail__language")
    list_filter = ("date_taken", "detail__language")
