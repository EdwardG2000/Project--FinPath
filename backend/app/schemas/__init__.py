from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, BadgeType

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    role: UserRole
    created_at: datetime
    current_streak: int
    longest_streak: int
    model_config = {"from_attributes": True}

class ModuleCreate(BaseModel):
    title: str
    description: str
    order_index: int = 0
    is_published: bool = True

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    is_published: Optional[bool] = None

class ModuleOut(BaseModel):
    id: int
    title: str
    description: str
    order_index: int
    is_published: bool
    created_at: datetime
    lesson_count: int = 0
    quiz_question_count: int = 0
    model_config = {"from_attributes": True}

class ModuleWithProgress(ModuleOut):
    completed_lessons: int = 0
    completion_pct: float = 0.0
    best_quiz_score: Optional[float] = None

class LessonCreate(BaseModel):
    module_id: int
    title: str
    content: str
    key_takeaways: Optional[str] = None
    order_index: int = 0
    estimated_minutes: int = 5
    is_published: bool = True

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    key_takeaways: Optional[str] = None
    order_index: Optional[int] = None
    estimated_minutes: Optional[int] = None
    is_published: Optional[bool] = None

class LessonOut(BaseModel):
    id: int
    module_id: int
    title: str
    content: str
    key_takeaways: Optional[str]
    order_index: int
    estimated_minutes: int
    is_published: bool
    model_config = {"from_attributes": True}

class LessonWithCompletion(LessonOut):
    is_completed: bool = False

class QuizQuestionCreate(BaseModel):
    module_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    explanation: str
    order_index: int = 0

class QuizQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_option: Optional[str] = None
    explanation: Optional[str] = None
    order_index: Optional[int] = None

class QuizQuestionOut(BaseModel):
    id: int
    module_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    order_index: int
    model_config = {"from_attributes": True}

class QuizQuestionAdmin(QuizQuestionOut):
    correct_option: str
    explanation: str

class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str

class QuizSubmitRequest(BaseModel):
    answers: List[AnswerSubmit]

class AnswerResult(BaseModel):
    question_id: int
    selected_option: str
    correct_option: str
    is_correct: bool
    explanation: str

class QuizSubmitResponse(BaseModel):
    attempt_id: int
    score: float
    total_questions: int
    correct_answers: int
    results: List[AnswerResult]
    new_badges: List[str] = []

class BadgeOut(BaseModel):
    badge_type: str
    earned_at: datetime
    model_config = {"from_attributes": True}

class ProgressOverview(BaseModel):
    overall_completion_pct: float
    total_lessons: int
    completed_lessons: int
    average_quiz_score: Optional[float]
    last_activity_at: Optional[datetime]
    current_streak: int
    longest_streak: int
    badges: List[BadgeOut]
    modules: List[ModuleWithProgress]

class CoachRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class CoachResponse(BaseModel):
    response: str
    conversation_id: str
    disclaimer: str = "Educational only — not financial advice."
