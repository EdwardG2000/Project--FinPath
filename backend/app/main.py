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

SEED_MODULES = [
    {
        "title": "Credit Score Basics",
        "description": "Understand what a credit score is, how it is calculated in the UK, and why it matters for your financial life.",
        "order_index": 1,
        "lessons": [
            {
                "title": "What is a Credit Score?",
                "order_index": 1,
                "estimated_minutes": 5,
                "content": "## What is a Credit Score?\n\nA **credit score** is a number that lenders use to assess how likely you are to repay borrowed money. In the UK, the main credit reference agencies are **Experian**, **Equifax**, and **TransUnion** — each with their own scoring scale.\n\n### UK Credit Score Ranges\n\nExperian scores range from 0 to 999, where 881 to 999 is considered excellent. Equifax scores range from 0 to 1000, and TransUnion from 0 to 710.\n\n### Why Does It Matter?\n\nYour credit score affects whether lenders approve your applications for credit cards, loans and mortgages. It also affects the interest rates you are offered. A higher score means cheaper borrowing.\n\n### The Golden Rule\n\nYou do not have one universal score. Each CRA holds slightly different data and uses different models. Always check all three if you are planning a major application.",
                "key_takeaways": "Credit scores in the UK range from 0 to 999 with Experian. Higher scores mean better loan terms. Three main CRAs: Experian, Equifax, TransUnion. Your score affects borrowing costs, renting, and sometimes employment.",
            },
            {
                "title": "What Affects Your Credit Score?",
                "order_index": 2,
                "estimated_minutes": 6,
                "content": "## What Affects Your Credit Score?\n\nYour credit score is built from data in your credit report. Here are the key factors:\n\n### 1. Payment History\n\nPaying bills on time is the single biggest factor. Even one missed payment can drop your score significantly and stays on file for **6 years**.\n\n### 2. Credit Utilisation\n\nThis is how much of your available credit limit you are using. If you have a £1,000 credit card limit and owe £800, your utilisation is 80% which looks risky to lenders. Keep utilisation below 30% for a healthy score.\n\n### 3. Length of Credit History\n\nOlder accounts show a longer track record. Closing old accounts can actually hurt your score.\n\n### 4. New Credit Applications\n\nEach time you apply for credit, lenders perform a **hard search** which temporarily dips your score. Multiple hard searches in a short period is a red flag.\n\n### 5. Electoral Roll Registration\n\nBeing registered to vote at your current address is a quick win for your score. Do it at gov.uk/register-to-vote.",
                "key_takeaways": "Payment history is most important. Keep credit utilisation under 30%. Register on the electoral roll. Avoid multiple credit applications in a short period.",
            },
            {
                "title": "How to Check Your Credit Score for Free",
                "order_index": 3,
                "estimated_minutes": 4,
                "content": "## How to Check Your Credit Score for Free\n\nIn the UK, you have the legal right to see your credit report. Here are the free options:\n\n### Free Credit Report Services\n\n- **ClearScore** uses Equifax data, free and updated weekly\n- **Credit Karma** uses TransUnion data, completely free\n- **MSE Credit Club** uses Experian data, completely free\n\n### What to Look For\n\nWhen checking your report, look for:\n- Any accounts you do not recognise which could indicate fraud\n- Incorrect addresses or personal details\n- Missed payments you thought were paid\n- Old defaults that should have dropped off after 6 years\n\n### Dispute Errors\n\nIf you find errors, contact the CRA directly. They must investigate within 28 days and correct genuine mistakes.\n\nChecking your own credit score is a **soft search** and does NOT affect your score.",
                "key_takeaways": "Check your credit for free via ClearScore, Credit Karma, or MSE Credit Club. Always look for errors. Checking your own score does not hurt it. Errors can be disputed within 28 days.",
            },
        ],
        "quiz_questions": [
            {
                "question_text": "Which UK credit reference agency uses a score range of 0 to 999?",
                "option_a": "Equifax",
                "option_b": "TransUnion",
                "option_c": "Experian",
                "option_d": "ClearScore",
                "correct_option": "c",
                "explanation": "Experian uses a score range of 0 to 999, where 881 to 999 is considered excellent. ClearScore is not a credit reference agency — it is a free service that uses Equifax data.",
                "order_index": 1,
            },
            {
                "question_text": "What credit utilisation percentage is generally recommended to maintain a healthy credit score?",
                "option_a": "Below 70%",
                "option_b": "Below 50%",
                "option_c": "Below 30%",
                "option_d": "Below 10%",
                "correct_option": "c",
                "explanation": "Keeping your credit utilisation below 30% is widely recommended. Using 80% or more of your limit can signal financial stress to lenders.",
                "order_index": 2,
            },
            {
                "question_text": "How does checking your own credit score affect your credit file?",
                "option_a": "It creates a hard search and lowers your score",
                "option_b": "It creates a soft search and does not affect your score",
                "option_c": "It improves your score by demonstrating responsibility",
                "option_d": "It has no record kept at all",
                "correct_option": "b",
                "explanation": "Checking your own credit report is a soft search and has no impact on your score. Only applications for credit create hard searches that can temporarily lower your score.",
                "order_index": 3,
            },
            {
                "question_text": "For how many years does a missed payment typically stay on your UK credit file?",
                "option_a": "2 years",
                "option_b": "4 years",
                "option_c": "6 years",
                "option_d": "10 years",
                "correct_option": "c",
                "explanation": "Most negative information including missed payments, defaults, and CCJs stays on your UK credit file for 6 years from the date it was recorded.",
                "order_index": 4,
            },
        ],
    },
    {
        "title": "Understanding APR & Interest",
        "description": "Learn how Annual Percentage Rate works, how interest is calculated, and how to compare credit products effectively.",
        "order_index": 2,
        "lessons": [
            {
                "title": "What is APR?",
                "order_index": 1,
                "estimated_minutes": 5,
                "content": "## What is APR?\n\nAPR stands for **Annual Percentage Rate**. It is the standardised way to express the total yearly cost of borrowing money, including both the interest rate and any mandatory fees.\n\n### Why APR Matters\n\nAPR lets you compare different credit products on a like-for-like basis. Without it, a loan with a low interest rate but high fees could actually cost more than one with a higher rate but no fees.\n\n### Representative APR vs Personal APR\n\nWhen you see an advert for credit, you will often see **Representative 19.9% APR**. This means at least 51% of accepted applicants get this rate or better. Your actual APR may be higher based on your credit score.\n\n### Simple vs Compound Interest\n\n- **Simple interest** is calculated only on the original amount borrowed\n- **Compound interest** is calculated on the balance including accumulated interest\n\nMost credit cards in the UK use compound interest, which means debt can grow quickly if you only make minimum payments.",
                "key_takeaways": "APR is the standardised yearly cost of borrowing including fees. Representative APR applies to at least 51% of applicants. Your personal APR may differ. Compound interest grows debt faster than simple interest.",
            },
            {
                "title": "How Credit Card Interest Works",
                "order_index": 2,
                "estimated_minutes": 6,
                "content": "## How Credit Card Interest Works\n\nCredit cards can be powerful financial tools or expensive debt traps depending on how you use them.\n\n### The Grace Period\n\nMost UK credit cards offer a **grace period** of around 55 days during which you pay no interest if you pay your full balance by the due date each month.\n\n### What Happens if You Do Not Pay in Full?\n\nIf you carry a balance, you will pay interest on the remaining amount and any new purchases from the date of purchase.\n\n### The Minimum Payment Trap\n\nPaying only the minimum each month is very expensive. For example on a £1,000 balance at 22.9% APR:\n\n- Minimum payments only: 7 years to repay, £850 in interest\n- £50 per month: 2.5 years to repay, £450 in interest\n- £100 per month: 11 months to repay, £100 in interest\n\n### 0% Purchase Periods\n\nMany cards offer 0% interest for an introductory period such as 12 months. This can be useful but the rate jumps to the standard APR after the period ends.",
                "key_takeaways": "Pay your full balance each month to avoid interest. Minimum payments are very expensive long term. 0% deals end so plan to pay off before then. Interest compounds on unpaid balances.",
            },
        ],
        "quiz_questions": [
            {
                "question_text": "What does APR stand for?",
                "option_a": "Annual Payment Rate",
                "option_b": "Annual Percentage Rate",
                "option_c": "Adjusted Personal Rate",
                "option_d": "Average Purchase Rate",
                "correct_option": "b",
                "explanation": "APR stands for Annual Percentage Rate. It is the standardised measure of the yearly cost of borrowing, including interest and mandatory fees.",
                "order_index": 1,
            },
            {
                "question_text": "When a lender advertises a Representative 19.9% APR, what does this mean?",
                "option_a": "All applicants will receive exactly 19.9% APR",
                "option_b": "At least 51% of accepted applicants will receive this rate or better",
                "option_c": "The average APR across all customers is 19.9%",
                "option_d": "This is the best rate available given only to top credit scores",
                "correct_option": "b",
                "explanation": "UK regulations require that the Representative APR is offered to at least 51% of accepted applicants. Your personal APR could be higher based on your credit profile.",
                "order_index": 2,
            },
            {
                "question_text": "If you pay your credit card balance in full each month, how much interest do you typically pay?",
                "option_a": "The standard APR rate",
                "option_b": "Half the standard APR rate",
                "option_c": "No interest at all",
                "option_d": "A small admin fee only",
                "correct_option": "c",
                "explanation": "Most UK credit cards have a grace period. If you pay your statement balance in full by the due date, you pay zero interest.",
                "order_index": 3,
            },
        ],
    },
    {
        "title": "Building Credit from Scratch",
        "description": "Practical strategies for young adults to build a positive credit history when they are just starting out.",
        "order_index": 3,
        "lessons": [
            {
                "title": "Why Young People Have Low Credit Scores",
                "order_index": 1,
                "estimated_minutes": 4,
                "content": "## Why Young People Have Low Credit Scores\n\nIf you are 18 to 25 and have a low or no credit score, you are not alone and it is not because you have done anything wrong.\n\n### The Thin File Problem\n\nA thin file means you do not have enough credit history for lenders to assess you. No history means uncertain risk which leads to rejection or high rates.\n\n### Common Reasons for a Thin File\n\n- Never had a credit card or loan\n- Recently moved to the UK\n- Always used debit cards which are great for budgeting but invisible to CRAs\n- Not on the electoral roll\n\n### The Catch-22\n\nYou need credit to build credit history, but you need credit history to get credit. This is the classic first-time borrower dilemma.\n\n### The Good News\n\nBuilding credit from scratch is entirely achievable. It just requires using the right tools deliberately and consistently.",
                "key_takeaways": "A thin credit file is not your fault — it just means you have not used credit yet. Debit cards do not build credit history. There are specific tools designed for credit building.",
            },
            {
                "title": "Practical Ways to Build Credit",
                "order_index": 2,
                "estimated_minutes": 7,
                "content": "## Practical Ways to Build Credit\n\nHere are proven strategies for building credit as a young adult in the UK:\n\n### 1. Get a Credit Builder Card\n\nThese are credit cards designed for people with limited credit history. They have low credit limits of £200 to £500 and higher APRs of around 30 to 40%. The key is to use them for small purchases and pay in full every month.\n\n### 2. Register on the Electoral Roll\n\nThis is free and immediate. Go to gov.uk/register-to-vote. It confirms your address and can noticeably boost your score within weeks.\n\n### 3. Mobile Phone Contract\n\nA monthly mobile contract involves a credit check and payments that get reported to CRAs. Consistently paying on time builds positive history.\n\n### 4. Experian Boost\n\nExperian Boost lets you link your bank account to get credit for regular payments like Netflix, Spotify, or council tax — things not normally reported.\n\n### The Timeline\n\nBuilding a solid credit history typically takes 6 to 12 months of consistent responsible use.",
                "key_takeaways": "Credit builder cards, electoral roll registration, and phone contracts are great starting points. Experian Boost can add everyday payments to your file. Consistent on-time payments for 6 to 12 months build solid history.",
            },
        ],
        "quiz_questions": [
            {
                "question_text": "What is a thin file in credit scoring?",
                "option_a": "A credit report showing many negative marks",
                "option_b": "A credit report with insufficient history for lenders to assess you",
                "option_c": "A credit report that has been fraudulently altered",
                "option_d": "A credit report for someone who has declared bankruptcy",
                "correct_option": "b",
                "explanation": "A thin file simply means there is not enough credit history on record. This is common for young people and does not mean you have had financial problems.",
                "order_index": 1,
            },
            {
                "question_text": "Which of the following does NOT help build your credit score?",
                "option_a": "Registering on the electoral roll",
                "option_b": "Getting a credit builder card and paying it in full each month",
                "option_c": "Using only a debit card for all purchases",
                "option_d": "Taking out a monthly mobile phone contract",
                "correct_option": "c",
                "explanation": "Debit cards are great for budgeting but they do not build credit history because they draw directly from your bank account with no borrowing or repayment record sent to CRAs.",
                "order_index": 2,
            },
        ],
    },
    {
        "title": "Debt Management",
        "description": "Learn how to manage debt responsibly, understand CCJs, and develop a plan to pay off what you owe.",
        "order_index": 4,
        "lessons": [
            {
                "title": "Types of Debt in the UK",
                "order_index": 1,
                "estimated_minutes": 5,
                "content": "## Types of Debt in the UK\n\nNot all debt is the same. Understanding the different types helps you prioritise which to pay off first.\n\n### Priority Debts\n\nThese have serious consequences if unpaid:\n- **Rent or mortgage** — risk of eviction or repossession\n- **Council tax** — can lead to bailiff action\n- **Energy bills** — risk of disconnection\n- **Court fines** — risk of enforcement action\n\n### Non-Priority Debts\n\nThese are serious but have less severe immediate consequences:\n- Credit cards\n- Personal loans\n- Overdrafts\n- Buy now pay later\n\n### What is a CCJ?\n\nA County Court Judgement is a court order issued when you fail to repay a debt. It stays on your credit file for 6 years and makes it very difficult to get credit, rent a flat, or sometimes even get a job.",
                "key_takeaways": "Always pay priority debts first. A CCJ stays on your credit file for 6 years. Non-priority debts are still serious and should be addressed. Ignoring debt makes it worse.",
            },
            {
                "title": "How to Create a Debt Payoff Plan",
                "order_index": 2,
                "estimated_minutes": 6,
                "content": "## How to Create a Debt Payoff Plan\n\nHaving a clear plan makes paying off debt much more manageable.\n\n### Step 1 — List All Your Debts\n\nWrite down every debt you have including the balance, interest rate, and minimum payment.\n\n### Step 2 — Choose a Strategy\n\n**Avalanche Method** — pay off the highest interest rate debt first. This saves the most money overall.\n\n**Snowball Method** — pay off the smallest balance first. This gives quick wins and keeps you motivated.\n\n### Step 3 — Make Minimum Payments on Everything\n\nAlways make at least the minimum payment on all debts to avoid late fees and credit score damage.\n\n### Step 4 — Throw Extra Money at Your Target Debt\n\nAny extra money beyond minimums goes entirely to your target debt until it is paid off, then move to the next one.\n\n### Free Help Available\n\nIf you are struggling with debt, free help is available from StepChange, National Debtline, and Citizens Advice.",
                "key_takeaways": "List all debts with balances and interest rates. The avalanche method saves the most money. The snowball method keeps you motivated. Free debt advice is available from StepChange and Citizens Advice.",
            },
        ],
        "quiz_questions": [
            {
                "question_text": "What does CCJ stand for?",
                "option_a": "Credit Collection Judgement",
                "option_b": "County Court Judgement",
                "option_c": "Central Credit Journal",
                "option_d": "Creditor Claim Judgement",
                "correct_option": "b",
                "explanation": "CCJ stands for County Court Judgement. It is a court order issued when you fail to repay a debt and stays on your credit file for 6 years.",
                "order_index": 1,
            },
            {
                "question_text": "Which debt payoff method saves the most money in interest?",
                "option_a": "The snowball method",
                "option_b": "The avalanche method",
                "option_c": "Paying all debts equally",
                "option_d": "Paying the newest debt first",
                "correct_option": "b",
                "explanation": "The avalanche method targets the highest interest rate debt first, which minimises the total interest paid over time.",
                "order_index": 2,
            },
            {
                "question_text": "Which of the following is a priority debt in the UK?",
                "option_a": "Credit card balance",
                "option_b": "Personal loan",
                "option_c": "Council tax",
                "option_d": "Overdraft",
                "correct_option": "c",
                "explanation": "Council tax is a priority debt because non-payment can lead to bailiff action. Credit cards, personal loans, and overdrafts are non-priority debts.",
                "order_index": 3,
            },
        ],
    },
    {
        "title": "Buy Now Pay Later",
        "description": "Understand how BNPL products like Klarna and Clearpay work, their risks, and how they affect your credit file.",
        "order_index": 5,
        "lessons": [
            {
                "title": "How Buy Now Pay Later Works",
                "order_index": 1,
                "estimated_minutes": 5,
                "content": "## How Buy Now Pay Later Works\n\nBuy Now Pay Later or BNPL lets you purchase something immediately and pay for it later, usually in instalments.\n\n### Popular UK BNPL Providers\n\n- **Klarna** — pay in 3 instalments or pay in 30 days\n- **Clearpay** — pay in 4 fortnightly instalments\n- **Laybuy** — pay in 6 weekly instalments\n\n### How It Seems\n\nBNPL feels like free money. There is often no interest if you pay on time. It is quick and easy to use at checkout.\n\n### How It Actually Works\n\nBNPL providers make money from late fees and from merchants who pay them to offer the service. The ease of use encourages overspending.\n\n### The Credit Check Question\n\nMost BNPL providers do a soft credit check when you apply so it does not affect your score. However missed payments can be reported to CRAs and damage your credit file.",
                "key_takeaways": "BNPL splits payments into instalments. Popular providers include Klarna and Clearpay. Missed payments can damage your credit score. BNPL makes it easy to overspend.",
            },
            {
                "title": "The Risks of Buy Now Pay Later",
                "order_index": 2,
                "estimated_minutes": 5,
                "content": "## The Risks of Buy Now Pay Later\n\nBNPL is increasingly popular with young adults but comes with real risks that are not always obvious.\n\n### Risk 1 — Easy to Lose Track\n\nUsing BNPL across multiple providers means you can quickly have several repayment schedules running at once, making it hard to track what you owe.\n\n### Risk 2 — Late Fees\n\nMissed payments trigger late fees which can add up quickly. Some providers charge a flat fee per missed payment.\n\n### Risk 3 — Credit File Damage\n\nFrom 2022 the FCA announced plans to regulate BNPL. As regulation increases, more providers will report to CRAs meaning missed payments will damage your credit score.\n\n### Risk 4 — Encourages Overspending\n\nBNPL makes expensive items feel affordable by hiding the true cost. This can lead to debt accumulation.\n\n### The Rule of Thumb\n\nOnly use BNPL if you have the money to pay for the item right now but prefer to spread the cost. Never use it to buy something you cannot actually afford.",
                "key_takeaways": "BNPL can lead to losing track of multiple repayments. Late fees add up quickly. Regulation is increasing and missed payments will affect credit scores. Only use BNPL if you can afford the item outright.",
            },
        ],
        "quiz_questions": [
            {
                "question_text": "Which of the following is a popular UK Buy Now Pay Later provider?",
                "option_a": "Monzo",
                "option_b": "Klarna",
                "option_c": "NatWest",
                "option_d": "Experian",
                "correct_option": "b",
                "explanation": "Klarna is one of the most popular BNPL providers in the UK, offering pay in 3 instalments or pay in 30 days options.",
                "order_index": 1,
            },
            {
                "question_text": "What is the safest way to use Buy Now Pay Later?",
                "option_a": "Use it for every purchase to spread costs",
                "option_b": "Only use it when you cannot afford something",
                "option_c": "Only use it when you already have the money to pay for the item",
                "option_d": "Use multiple BNPL providers at once",
                "correct_option": "c",
                "explanation": "The safest approach is to only use BNPL when you already have the money available. This way you are just choosing how to pay rather than taking on debt you cannot afford.",
                "order_index": 2,
            },
        ],
    },
]


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
        for mod_data in SEED_MODULES:
            module = Module(title=mod_data["title"], description=mod_data["description"], order_index=mod_data["order_index"], is_published=True)
            db.add(module)
            await db.flush()
            for lesson_data in mod_data.get("lessons", []):
                lesson = Lesson(module_id=module.id, title=lesson_data["title"], content=lesson_data["content"], key_takeaways=lesson_data.get("key_takeaways"), order_index=lesson_data["order_index"], estimated_minutes=lesson_data["estimated_minutes"], is_published=True)
                db.add(lesson)
            for q_data in mod_data.get("quiz_questions", []):
                question = QuizQuestion(module_id=module.id, question_text=q_data["question_text"], option_a=q_data["option_a"], option_b=q_data["option_b"], option_c=q_data["option_c"], option_d=q_data["option_d"], correct_option=q_data["correct_option"], explanation=q_data["explanation"], order_index=q_data["order_index"])
                db.add(question)
        await db.commit()
        print("[Seed] Done!")