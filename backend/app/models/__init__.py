from __future__ import annotations
import enum
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import String, Text, Integer, Float, Boolean, ForeignKey, DateTime, Date, Enum as SAEnum, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class BadgeType(str, enum.Enum):
    FIRST_LESSON = "FIRST_LESSON"
    FIRST_QUIZ = "FIRST_QUIZ"
    STREAK_3 = "STREAK_3"
    STREAK_7 = "STREAK_7"
    SCORE_80 = "SCORE_80"
    COMPLETE_FIRST_MODULE = "COMPLETE_FIRST_MODULE"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.user, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_activity_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_streak_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    lesson_completions: Mapped[List[LessonCompletion]] = relationship(back_populates="user", cascade="all, delete-orphan")
    quiz_attempts: Mapped[List[QuizAttempt]] = relationship(back_populates="user", cascade="all, delete-orphan")
    user_badges: Mapped[List[UserBadge]] = relationship(back_populates="user", cascade="all, delete-orphan")
    chat_logs: Mapped[List[AIChatLog]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Module(Base):
    __tablename__ = "modules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    lessons: Mapped[List[Lesson]] = relationship(back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order_index")
    quiz_questions: Mapped[List[QuizQuestion]] = relationship(back_populates="module", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    key_takeaways: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=5)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    module: Mapped[Module] = relationship(back_populates="lessons")
    completions: Mapped[List[LessonCompletion]] = relationship(back_populates="lesson", cascade="all, delete-orphan")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"), nullable=False, index=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    option_a: Mapped[str] = mapped_column(String(500), nullable=False)
    option_b: Mapped[str] = mapped_column(String(500), nullable=False)
    option_c: Mapped[str] = mapped_column(String(500), nullable=False)
    option_d: Mapped[str] = mapped_column(String(500), nullable=False)
    correct_option: Mapped[str] = mapped_column(String(1), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    module: Mapped[Module] = relationship(back_populates="quiz_questions")
    attempt_answers: Mapped[List[AttemptAnswer]] = relationship(back_populates="question", cascade="all, delete-orphan")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user: Mapped[User] = relationship(back_populates="quiz_attempts")
    answers: Mapped[List[AttemptAnswer]] = relationship(back_populates="attempt", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_quiz_attempts_user_module", "user_id", "module_id"),)

class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("quiz_attempts.id"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("quiz_questions.id"), nullable=False)
    selected_option: Mapped[str] = mapped_column(String(1), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    attempt: Mapped[QuizAttempt] = relationship(back_populates="answers")
    question: Mapped[QuizQuestion] = relationship(back_populates="attempt_answers")

class LessonCompletion(Base):
    __tablename__ = "lesson_completions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False, index=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user: Mapped[User] = relationship(back_populates="lesson_completions")
    lesson: Mapped[Lesson] = relationship(back_populates="completions")
    __table_args__ = (Index("ix_lesson_completions_user_lesson", "user_id", "lesson_id"),)

class UserBadge(Base):
    __tablename__ = "user_badges"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    badge_type: Mapped[BadgeType] = mapped_column(SAEnum(BadgeType), nullable=False)
    earned_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user: Mapped[User] = relationship(back_populates="user_badges")
    __table_args__ = (Index("ix_user_badges_user_badge", "user_id", "badge_type", unique=True),)

class AIChatLog(Base):
    __tablename__ = "ai_chat_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    conversation_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    assistant_response: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user: Mapped[User] = relationship(back_populates="chat_logs")
