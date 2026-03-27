from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, AsyncSessionLocal
from app.models import Module, Lesson, QuizQuestion, User, UserRole
from app.services.auth import hash_password
from app.routers import auth, modules, lessons, quiz, progress, ai_coach

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_data()
    yield

app = FastAPI(title="FinPath API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(modules.router)
app.include_router(lessons.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(ai_coach.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

async def seed_data():
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        result = await db.execute(select(Module).limit(1))
        if result.scalar_one_or_none():
            return
        print("[Seed] Seeding initial data...")
        admin = User(email="admin@finpath.co.uk", username="admin", hashed_password=hash_password("admin1234"), role=UserRole.admin)
        demo = User(email="demo@finpath.co.uk", username="demo_user", hashed_password=hash_password("demo1234"), role=UserRole.user)
        db.add(admin)
        db.add(demo)
        await db.flush()
        module = Module(title="Credit Score Basics", description="Understand what a credit score is and why it matters.", order_index=1, is_published=True)
        db.add(module)
        await db.flush()
        lessons = [
            Lesson(module_id=module.id, title="What is a Credit Score?", content="## What is a Credit Score?\n\nA credit score is a number that lenders use to assess how likely you are to repay borrowed money. In the UK, the main credit reference agencies are Experian, Equifax, and TransUnion.\n\n### Why Does It Matter?\n\nYour credit score affects whether lenders approve your applications and the interest rates you are offered. A higher score means better loan terms.", key_takeaways="Credit scores range from 0-999 with Experian. Higher scores mean better loan terms. Three main CRAs in the UK.", order_index=1, estimated_minutes=5, is_published=True),
            Lesson(module_id=module.id, title="What Affects Your Credit Score?", content="## What Affects Your Credit Score?\n\n### Payment History\nPaying bills on time is the biggest factor. Even one missed payment can drop your score and stays on file for 6 years.\n\n### Credit Utilisation\nKeep usage below 30% of your credit limit.\n\n### Electoral Roll\nRegister to vote at gov.uk to boost your score quickly.", key_takeaways="Payment history is most important. Keep utilisation under 30%. Register on the electoral roll.", order_index=2, estimated_minutes=5, is_published=True),
        ]
        for lesson in lessons:
            db.add(lesson)
        await db.flush()
        questions = [
            QuizQuestion(module_id=module.id, question_text="Which UK credit reference agency uses a score range of 0-999?", option_a="Equifax", option_b="TransUnion", option_c="Experian", option_d="ClearScore", correct_option="c", explanation="Experian uses a score range of 0-999 where 881-999 is excellent.", order_index=1),
            QuizQuestion(module_id=module.id, question_text="What credit utilisation percentage is recommended for a healthy score?", option_a="Below 70%", option_b="Below 50%", option_c="Below 30%", option_d="Below 10%", correct_option="c", explanation="Keeping utilisation below 30% is widely recommended by credit experts.", order_index=2),
        ]
        for q in questions:
            db.add(q)
        await db.commit()
        print("[Seed] Done!")
