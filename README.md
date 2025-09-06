# AI Quiz Project (Django + Google Gemini AI)

A Django-based quiz platform where users can take manually created quizzes or generate AI-based quizzes using Google Gemini AI. The project also tracks quiz history per user.

---

## Features

- **User Authentication:** Login, Logout, Register.
- **Manual Quizzes:** Create and take quizzes in multiple languages (Python, JavaScript, C).
- **AI Generated Quizzes:** Generate quizzes using Google Gemini AI in multiple languages and levels.
- **Quiz History:** Display the last 20 quizzes attempted by a user.
- **Responsive UI:** Quiz and history displayed in a flex layout (80% quiz / 20% history).
- **Admin Site :** Along with the Default admin site also two pages for manual quiz generation and validation at localhost/quiz/.

---

## Technologies

- **Backend:** Django 5.2
- **Frontend:** HTML, CSS
- **AI Integration:** Google Gemini AI (`google.generativeai` package)
- **Database:** SQLite (default, can be changed)
- **Environment Management:** `python-dotenv` for environment variables

---


## Setup

- **Clone repo** 
- **make .env file in root** set GEMINI_API_KEY in this (get it from  https://aistudio.google.com/app/apikey)

---

## Usage

- **Login/Register** to start taking quizzes.

- **Manual Quizzes**: Use the language dropdown to select and attempt a quiz.

- **AI Quizzes**: Select language and difficulty level, then click AI Based Quiz.

- **History**: Your last 20 quizzes will appear on the right side of the screen.


---

## Notes

Ensure your Gemini API key is valid.

AI quizzes normalize boolean values for correct options to prevent display issues.

Quiz results highlight correct answers in green and wrong answers in red.

History section shows last 20 quizzes in a sidebar.


### Made by Himanshu (hs024)