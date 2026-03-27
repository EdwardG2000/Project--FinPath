from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models import QuizQuestion, QuizAttempt, AttemptAnswer, User
from app.schemas import QuizQuestionCreate, QuizQuestionUpdate, QuizQuestionOut, QuizQuestionAdmin, QuizSubmitRequest, QuizSubmitResponse, AnswerResult
from app.services.auth import get_current_user, require_admin
from app.services.gamification import update_streak, check_and_award_badges

router = APIRouter(prefix="/quiz", tags=["quiz"])

@router.get("/{module_id}", response_model=List[QuizQuestionOut])
async def get_quiz_questions(module_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(QuizQuestion).where(QuizQuestion.module_id == module_id).order_by(QuizQuestion.order_index))
    return result.scalars().all()

@router.post("/{module_id}/submit", response_model=QuizSubmitResponse)
async def submit_quiz(module_id: int, body: QuizSubmitRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(QuizQuestion).where(QuizQuestion.module_id == module_id))
    questions = {q.id: q for q in result.scalars().all()}
    if not questions:
        raise HTTPException(status_code=404, detail="No quiz questions found for this module")
    results = []
    correct_count = 0
    for answer in body.answers:
        q = questions.get(answer.question_id)
        if not q:
            continue
        is_correct = answer.selected_option.lower() == q.correct_option.lower()
        if is_correct:
            correct_count += 1
        results.append(AnswerResult(question_id=q.id, selected_option=answer.selected_option, correct_option=q.correct_option, is_correct=is_correct, explanation=q.explanation))
    total = len(body.answers)
    score = (correct_count / total * 100) if total > 0 else 0
    attempt = QuizAttempt(user_id=current_user.id, module_id=module_id, score=score, total_questions=total, correct_answers=correct_count)
    db.add(attempt)
    await db.flush()
    for r in results:
        db.add(AttemptAnswer(attempt_id=attempt.id, question_id=r.question_id, selected_option=r.selected_option, is_correct=r.is_correct))
    await update_streak(current_user, db)
    new_badges = await check_and_award_badges(current_user, db, {"quiz_score": score})
    await db.commit()
    return QuizSubmitResponse(attempt_id=attempt.id, score=score, total_questions=total, correct_answers=correct_count, results=results, new_badges=new_badges)

@router.get("/admin/questions", response_model=List[QuizQuestionAdmin])
async def list_all_questions(db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(QuizQuestion).order_by(QuizQuestion.module_id, QuizQuestion.order_index))
    return result.scalars().all()

@router.post("/questions", response_model=QuizQuestionAdmin, status_code=201)
async def create_question(body: QuizQuestionCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    question = QuizQuestion(**body.model_dump())
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question

@router.put("/questions/{question_id}", response_model=QuizQuestionAdmin)
async def update_question(question_id: int, body: QuizQuestionUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(QuizQuestion).where(QuizQuestion.id == question_id))
    q = result.scalar_one_or_none()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(q, k, v)
    await db.commit()
    await db.refresh(q)
    return q

@router.delete("/questions/{question_id}", status_code=204)
async def delete_question(question_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(QuizQuestion).where(QuizQuestion.id == question_id))
    q = result.scalar_one_or_none()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    await db.delete(q)
    await db.commit()
