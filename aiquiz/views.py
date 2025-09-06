import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from quiz.models import Quiz, QuizHistory

# configure Gemini with your API key (store in settings.py or env)
genai.configure(api_key=settings.GEMINI_API_KEY)

@login_required
def ai_quiz(request, language="Python",level="beginner"):
    print("Generating AI quiz for language:", language)
    if request.method == "POST":
        # when user submits answers
        quiz_id = request.POST.get("quiz_id")
        quiz = Quiz.objects.get(id=quiz_id)

        score, results = 0, {}
        for q_text, options in quiz.questions.items():
            selected = request.POST.get(q_text)
            correct_index = None

            # normalize options
            normalized = []
            for idx, (text, exp, is_c) in enumerate(options):
                if isinstance(is_c, str):
                    is_c = is_c.lower() == "true"
                normalized.append([text, exp, is_c])
                if is_c:
                    correct_index = str(idx)   # store as string like manual

            options = normalized

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
        history = QuizHistory.objects.filter(user=request.user).order_by("-date_taken")[:20]

        return render(request, "home.html", {
            "quiz": quiz,
            "results": results,
            "score": score,
            "total": len(quiz.questions),
            "show_result": True,
            "history": history,
        })


    # GET → generate quiz using Gemini
    prompt = f"""
    Generate 10 multiple-choice quiz questions about {language}.
    with the difficulty level of a {level} programmer.
    Format as JSON:
    {{
        "Question?": [
            ["Option1", "Explanation1", false],
            ["Option2", "Explanation2", true],
            ["Option3", "Explanation3", false],
            ["Option4", "Explanation4", false]
        ]
    }}
    example
    {{
        "What is the output of print(2**3)?": [
            ["5", "2 to the power of 3 is 8", false],
            ["6", "2 to the power of 3 is 8", false],
            ["8", "Correct! 2 to the power of 3 is 8", true],
            ["9", "2 to the power of 3 is 8", false]
        ],
        "Which keyword is used to define a function in Python?": [
            ["func", "Incorrect, use 'def'", false],
            ["define", "Incorrect, use 'def'", false],
            ["def", "Correct! 'def' is used to define functions", true],
            ["function", "Incorrect, use 'def'", false]
        ],
        "What data structure does Python use to implement a stack?": [
            ["List", "Correct! Lists can be used as stacks with append() and pop()", true],
            ["Dictionary", "Incorrect, dictionaries are key-value pairs", false],
            ["Tuple", "Incorrect, tuples are immutable sequences", false],
            ["Set", "Incorrect, sets are unordered collections of unique elements", false]
        ]
    }}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    import re, json

    raw_text = response.text.strip()

    # Remove markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```[a-zA-Z]*\n", "", raw_text)  # remove opening ```json or ```
        raw_text = re.sub(r"\n```$", "", raw_text)          # remove closing ```

    try:
        questions = json.loads(raw_text)
        # normalize AI response
        normalized_questions = {}
        for q_text, opts in questions.items():
            fixed = []
            for opt in opts:
                text, exp, is_c = opt
                if isinstance(is_c, str):
                    is_c = is_c.lower() == "true"
                fixed.append([text, exp, is_c])
            normalized_questions[q_text] = fixed
        questions = normalized_questions

    except Exception as e:
        print("Failed to parse AI response:", raw_text, e)
        return render(request, "home.html", {"quiz": None, "error": "Failed to parse AI response."})
    # Save AI quiz in DB
    quiz = Quiz.objects.create(language=language.upper(), questions=questions)
    history = QuizHistory.objects.filter(user=request.user).order_by("-date_taken")[:20]
    print("AI quiz generated:")
    return render(request, "home.html", {"quiz": quiz, "history": history})
