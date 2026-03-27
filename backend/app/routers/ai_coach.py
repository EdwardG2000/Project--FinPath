import uuid
from collections import defaultdict
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.schemas import CoachRequest, CoachResponse
from app.services.auth import get_current_user
from app.services.ai_coach import ask_coach

router = APIRouter(prefix="/ai", tags=["ai"])

_rate_store: dict = defaultdict(list)
RATE_LIMIT = 20
WINDOW_SECONDS = 3600

def _check_rate_limit(user_id: int) -> None:
    now = datetime.now(timezone.utc)
    _rate_store[user_id] = [t for t in _rate_store[user_id] if (now - t).total_seconds() < WINDOW_SECONDS]
    if len(_rate_store[user_id]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail=f"Rate limit reached. Max {RATE_LIMIT} messages per hour.")
    _rate_store[user_id].append(now)

@router.post("/coach", response_model=CoachResponse)
async def coach(body: CoachRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    _check_rate_limit(current_user.id)
    conversation_id = body.conversation_id or str(uuid.uuid4())
    response_text = await ask_coach(user_id=current_user.id, message=body.message, conversation_id=conversation_id, db=db)
    return CoachResponse(response=response_text, conversation_id=conversation_id)
