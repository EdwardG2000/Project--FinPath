from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.database import get_db
from app.models import Lesson, LessonCompletion, User
from app.schemas import LessonCreate, LessonUpdate, LessonOut, LessonWithCompletion
from app.services.auth import get_current_user, require_admin
from app.services.gamification import update_streak, check_and_award_badges

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/module/{module_id}", response_model=List[LessonWithCompletion])
async def list_lessons_for_module(module_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Lesson).where(Lesson.module_id == module_id, Lesson.is_published == True).order_by(Lesson.order_index))
    lessons = result.scalars().all()
    completed_r = await db.execute(select(LessonCompletion.lesson_id).where(LessonCompletion.user_id == current_user.id))
    completed_ids = {row[0] for row in completed_r.fetchall()}
    return [{**lesson.__dict__, "is_completed": lesson.id in completed_ids} for lesson in lessons]

@router.get("/{lesson_id}", response_model=LessonWithCompletion)
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    completed_r = await db.execute(select(LessonCompletion).where(LessonCompletion.user_id == current_user.id, LessonCompletion.lesson_id == lesson_id))
    return {**lesson.__dict__, "is_completed": completed_r.scalar_one_or_none() is not None}

@router.post("/{lesson_id}/complete")
async def complete_lesson(lesson_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    existing = await db.execute(select(LessonCompletion).where(LessonCompletion.user_id == current_user.id, LessonCompletion.lesson_id == lesson_id))
    if not existing.scalar_one_or_none():
        db.add(LessonCompletion(user_id=current_user.id, lesson_id=lesson_id))
    await update_streak(current_user, db)
    total_r = await db.execute(select(func.count()).where(Lesson.module_id == lesson.module_id, Lesson.is_published == True))
    total = total_r.scalar() or 0
    completed_r = await db.execute(select(func.count()).where(LessonCompletion.user_id == current_user.id, LessonCompletion.lesson_id.in_(select(Lesson.id).where(Lesson.module_id == lesson.module_id))))
    completed = (completed_r.scalar() or 0) + 1
    module_done = total > 0 and completed >= total
    new_badges = await check_and_award_badges(current_user, db, {"lesson_completed": True, "module_fully_complete": module_done})
    await db.commit()
    return {"success": True, "new_badges": new_badges, "module_completed": module_done}

@router.post("", response_model=LessonOut, status_code=201)
async def create_lesson(body: LessonCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    lesson = Lesson(**body.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson

@router.put("/{lesson_id}", response_model=LessonOut)
async def update_lesson(lesson_id: int, body: LessonUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(lesson, k, v)
    await db.commit()
    await db.refresh(lesson)
    return lesson

@router.delete("/{lesson_id}", status_code=204)
async def delete_lesson(lesson_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    await db.delete(lesson)
    await db.commit()
