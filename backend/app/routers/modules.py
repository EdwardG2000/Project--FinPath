from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.database import get_db
from app.models import Module, Lesson, QuizQuestion, User
from app.schemas import ModuleCreate, ModuleUpdate, ModuleOut
from app.services.auth import get_current_user, require_admin

router = APIRouter(prefix="/modules", tags=["modules"])

async def enrich_module(module: Module, db: AsyncSession) -> dict:
    lesson_count_r = await db.execute(select(func.count()).where(Lesson.module_id == module.id, Lesson.is_published == True))
    quiz_count_r = await db.execute(select(func.count()).where(QuizQuestion.module_id == module.id))
    d = {**module.__dict__, "lesson_count": lesson_count_r.scalar() or 0, "quiz_question_count": quiz_count_r.scalar() or 0}
    d.pop("_sa_instance_state", None)
    return d

@router.get("", response_model=List[ModuleOut])
async def list_modules(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Module).where(Module.is_published == True).order_by(Module.order_index))
    return [await enrich_module(m, db) for m in result.scalars().all()]

@router.get("/{module_id}", response_model=ModuleOut)
async def get_module(module_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return await enrich_module(module, db)

@router.post("", response_model=ModuleOut, status_code=201)
async def create_module(body: ModuleCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    module = Module(**body.model_dump())
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return await enrich_module(module, db)

@router.put("/{module_id}", response_model=ModuleOut)
async def update_module(module_id: int, body: ModuleUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(module, k, v)
    await db.commit()
    await db.refresh(module)
    return await enrich_module(module, db)

@router.delete("/{module_id}", status_code=204)
async def delete_module(module_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    await db.delete(module)
    await db.commit()
