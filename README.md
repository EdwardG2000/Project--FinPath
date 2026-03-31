# FinPath

A web app for learning UK financial literacy — built as my final year university project.

The idea came from noticing how little most people my age actually understand about credit scores, APR, debt, and things like Buy Now Pay Later. FinPath tries to fix that by making the learning feel more like a game than a textbook.

---

## Try it

**https://glistening-fairy-8a64da.netlify.app/login.html**

You can create a free account or use the demo credentials below.

| Email | Password |
|-------|----------|
| demo@finpath.co.uk | demo1234 |

---

## What it does

- Five modules covering credit scores, APR and interest, building credit from scratch, debt management, and Buy Now Pay Later
- 21 bite-sized lessons with structured content and key takeaways
- Module quizzes that unlock after completing all lessons
- XP system — earn 20 XP per lesson, level up from Beginner through to Diamond
- Daily streaks to encourage consistent learning
- Badge system — unlock achievements as you progress
- AI Money Coach powered by GPT-4, trained on the lesson content
- Leaderboard showing real user progress from the database
- Full user authentication with age verification (18+ only)

---

## Tech stack

**Frontend** — Vanilla HTML, CSS, JavaScript. No frameworks, kept deliberately simple for this project stage.

**Backend** — Python with FastAPI, SQLAlchemy for the database layer, asyncpg for async PostgreSQL connections, JWT for authentication, and the OpenAI API for the AI coach.

**Database** — PostgreSQL

**Hosting** — Frontend on Netlify, backend and database on Railway

---

## Project structure

```
/
├── login.html          Landing page and authentication
├── dashboard.html      User home screen
├── learn.html          Module selection
├── lesson.html         Lesson viewer with quiz popup
├── coach.html          AI Money Coach chat
├── leaderboard.html    Live leaderboard from database
├── profile.html        User stats and badges
├── styles.css          Main stylesheet
├── navbar.js           Shared navigation component
├── api.js              API client functions
├── gamification.js     XP, badges, streaks logic
├── background.js       Animated background
└── backend/
    └── app/
        ├── main.py         App entry point and seed data
        ├── database.py     Database connection
        ├── models/         SQLAlchemy models
        ├── schemas/        Pydantic schemas
        ├── routers/        API route handlers
        └── services/       Business logic
```

---

## API

Backend: https://project-finpath-production.up.railway.app

Interactive API docs: https://project-finpath-production.up.railway.app/docs

---

## Disclaimer

FinPath is built for educational purposes only. Nothing on the platform constitutes financial advice. Users are always directed to consult a qualified financial adviser before making any financial decisions.
