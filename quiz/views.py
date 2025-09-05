from django.shortcuts import render
from .models import Quiz

def create_quiz(request):
    n = 2 # number of questions
    if request.method == "POST":
        language = request.POST.get("language")
        questions = {}

        for i in range(1, n+1):
            q_text = request.POST.get(f"question{i}")
            options = []
            correct_answers = request.POST.getlist(f"q{i}_correct")  # list of correct indices

            for j in range(1, 5):
                opt = request.POST.get(f"q{i}_opt{j}")
                exp = request.POST.get(f"q{i}_exp{j}") or None
                is_correct = str(j) in correct_answers
                options.append([opt, exp, is_correct])

            questions[q_text] = options

        quiz = Quiz.objects.create(
            language=language,
            questions=questions
        )
        return render(request, "quiz_created.html", {"quiz": quiz})

    return render(request, "quiz_form.html", {"range10": range(1, n+1), "range4": range(1, 5)})








import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, QuizHistory
@login_required
def take_quiz(request, language=None):
    history = QuizHistory.objects.filter(user=request.user).order_by("-date_taken")[:20]
    if not language:  # no language selected yet
        return render(request, "home.html", {"quiz": None, "history": history})

    quizzes = Quiz.objects.filter(language=language.upper())
    if not quizzes.exists():
        return render(request, "home.html", {"quiz": None, "no_quiz": True, "history": history})

    if request.method == "POST":
        quiz_id = request.POST.get("quiz_id")
        quiz = Quiz.objects.filter(id=quiz_id, language=language.upper()).first()
        if not quiz:
            return render(request, "home.html", {"quiz": None, "no_quiz": True, "history": history})

        score = 0
        results = {}

        for q_text, options in quiz.questions.items():
            selected = request.POST.get(q_text)
            correct_index = None

            for idx, (opt, exp, is_correct) in enumerate(options):
                if is_correct:
                    correct_index = str(idx)

            is_correct_ans = (selected == correct_index)
            if is_correct_ans:
                score += 1

            results[q_text] = {
                "selected": int(selected) if selected else None,
                "correct": int(correct_index),
                "options": options,
                "is_correct": is_correct_ans,
            }

        QuizHistory.objects.create(user=request.user, score=score, detail=quiz)

        return render(request, "home.html", {
            "quiz": quiz,
            "results": results,
            "score": score,
            "total": len(quiz.questions),
            "show_result": True,
            "history": history
        })

    # GET → pick a random quiz for the language
    quiz = random.choice(list(quizzes))
    return render(request, "home.html", {"quiz": quiz, "history": history})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import QuizHistory
@login_required
def quiz_with_history(request):
    history = QuizHistory.objects.filter(user=request.user).order_by("-date_taken")[:20]
    return render(request, "history.html", {"history": history})
