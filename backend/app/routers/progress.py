from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.database import get_db
from app.models import User, Module, Lesson, LessonCompletion, QuizAttempt, UserBadge, UserRole
from app.schemas import ProgressOverview, ModuleWithProgress, BadgeOut
from app.services.auth import get_current_user

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("/overview", response_model=ProgressOverview)
async def get_progress_overview(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_r = await db.execute(select(func.count()).where(Lesson.is_published == True))
    total_lessons = total_r.scalar() or 0
    completed_r = await db.execute(select(func.count()).where(LessonCompletion.user_id == current_user.id))
    completed_lessons = completed_r.scalar() or 0
    overall_pct = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    avg_r = await db.execute(select(func.avg(QuizAttempt.score)).where(QuizAttempt.user_id == current_user.id))
    avg_score: Optional[float] = avg_r.scalar()
    badges_r = await db.execute(select(UserBadge).where(UserBadge.user_id == current_user.id).order_by(UserBadge.earned_at))
    badges = [BadgeOut.model_validate(b) for b in badges_r.scalars().all()]
    modules_r = await db.execute(select(Module).where(Module.is_published == True).order_by(Module.order_index))
    modules = modules_r.scalars().all()
    module_progress = []
    for m in modules:
        lesson_count_r = await db.execute(select(func.count()).where(Lesson.module_id == m.id, Lesson.is_published == True))
        lesson_count = lesson_count_r.scalar() or 0
        done_r = await db.execute(select(func.count()).where(LessonCompletion.user_id == current_user.id, LessonCompletion.lesson_id.in_(select(Lesson.id).where(Lesson.module_id == m.id))))
        completed = done_r.scalar() or 0
        best_score_r = await db.execute(select(func.max(QuizAttempt.score)).where(QuizAttempt.user_id == current_user.id, QuizAttempt.module_id == m.id))
        best_score = best_score_r.scalar()
        module_progress.append(ModuleWithProgress(
            id=m.id, title=m.title, description=m.description,
            order_index=m.order_index, is_published=m.is_published,
            created_at=m.created_at, lesson_count=lesson_count,
            quiz_question_count=0, completed_lessons=completed,
            completion_pct=(completed / lesson_count * 100) if lesson_count > 0 else 0,
            best_quiz_score=best_score,
        ))
    return ProgressOverview(
        overall_completion_pct=overall_pct, total_lessons=total_lessons,
        completed_lessons=completed_lessons, average_quiz_score=avg_score,
        last_activity_at=current_user.last_activity_at,
        current_streak=current_user.current_streak,
        longest_streak=current_user.longest_streak,
        badges=badges, modules=module_progress,
    )

@router.get("/leaderboard")
async def get_leaderboard(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    from sqlalchemy import select, func
    from app.models import LessonCompletion, QuizAttempt
    
    # Get all users
    users_result = await db.execute(select(User).where(User.role == UserRole.user))
    users = users_result.scalars().all()
    
    leaderboard = []
    for user in users:
        # Get completed lessons count
        lessons_result = await db.execute(
            select(func.count()).where(LessonCompletion.user_id == user.id)
        )
        lessons_done = lessons_result.scalar() or 0
        
        # Get best quiz scores total
        quiz_result = await db.execute(
            select(func.sum(QuizAttempt.score)).where(QuizAttempt.user_id == user.id)
        )
        quiz_total = quiz_result.scalar() or 0
        
        xp = (lessons_done * 20) + int(quiz_total / 10)
        
        leaderboard.append({
            "user_id": user.id,
            "username": user.username,
            "xp": xp,
            "lessons_done": lessons_done,
            "is_me": user.id == current_user.id
        })
    
    leaderboard.sort(key=lambda x: x["xp"], reverse=True)
    
    for i, entry in enumerate(leaderboard):
        entry["rank"] = i + 1
    
    return leaderboard
