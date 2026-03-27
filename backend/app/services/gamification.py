from datetime import date, datetime, timezone
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import User, UserBadge, BadgeType, LessonCompletion, QuizAttempt

async def update_streak(user: User, db: AsyncSession) -> None:
    today = date.today()
    if user.last_streak_date == today:
        return
    if user.last_streak_date is None:
        user.current_streak = 1
    elif (today - user.last_streak_date).days == 1:
        user.current_streak += 1
    elif (today - user.last_streak_date).days > 1:
        user.current_streak = 1
    user.last_streak_date = today
    user.last_activity_at = datetime.now(timezone.utc)
    if user.current_streak > user.longest_streak:
        user.longest_streak = user.current_streak

async def award_badge(user: User, badge_type: BadgeType, db: AsyncSession) -> bool:
    existing = await db.execute(
        select(UserBadge).where(UserBadge.user_id == user.id, UserBadge.badge_type == badge_type)
    )
    if existing.scalar_one_or_none():
        return False
    badge = UserBadge(user_id=user.id, badge_type=badge_type)
    db.add(badge)
    return True

async def check_and_award_badges(user: User, db: AsyncSession, context: dict) -> List[str]:
    new_badges: List[str] = []
    if context.get("lesson_completed"):
        lesson_count_result = await db.execute(
            select(func.count()).where(LessonCompletion.user_id == user.id)
        )
        if (lesson_count_result.scalar() or 0) == 1:
            if await award_badge(user, BadgeType.FIRST_LESSON, db):
                new_badges.append(BadgeType.FIRST_LESSON.value)
    if context.get("quiz_score") is not None:
        quiz_count_result = await db.execute(
            select(func.count()).where(QuizAttempt.user_id == user.id)
        )
        if (quiz_count_result.scalar() or 0) == 1:
            if await award_badge(user, BadgeType.FIRST_QUIZ, db):
                new_badges.append(BadgeType.FIRST_QUIZ.value)
        if context["quiz_score"] >= 80:
            if await award_badge(user, BadgeType.SCORE_80, db):
                new_badges.append(BadgeType.SCORE_80.value)
    if user.current_streak >= 3:
        if await award_badge(user, BadgeType.STREAK_3, db):
            new_badges.append(BadgeType.STREAK_3.value)
    if user.current_streak >= 7:
        if await award_badge(user, BadgeType.STREAK_7, db):
            new_badges.append(BadgeType.STREAK_7.value)
    if context.get("module_fully_complete"):
        if await award_badge(user, BadgeType.COMPLETE_FIRST_MODULE, db):
            new_badges.append(BadgeType.COMPLETE_FIRST_MODULE.value)
    return new_badges
