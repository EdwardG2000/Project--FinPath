from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Lesson, AIChatLog
from app.config import settings

_chunks: List[dict] = []
_embeddings_ready = False

def _chunk_lesson(lesson: Lesson) -> List[str]:
    words = lesson.content.split()
    chunks = []
    for i in range(0, len(words), 300):
        chunk = " ".join(words[i:i + 300])
        chunks.append(chunk)
    if lesson.key_takeaways:
        chunks.append(lesson.key_takeaways)
    return chunks

def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x ** 2 for x in a) ** 0.5
    norm_b = sum(x ** 2 for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

async def build_index(db: AsyncSession) -> None:
    global _chunks, _embeddings_ready
    if not settings.OPENAI_API_KEY:
        _embeddings_ready = False
        return
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        result = await db.execute(select(Lesson).where(Lesson.is_published == True))
        lessons = result.scalars().all()
        new_chunks = []
        for lesson in lessons:
            for chunk_text in _chunk_lesson(lesson):
                if chunk_text.strip():
                    new_chunks.append({"lesson_id": lesson.id, "lesson_title": lesson.title, "text": chunk_text, "embedding": None})
        texts = [c["text"] for c in new_chunks]
        if texts:
            response = await client.embeddings.create(model="text-embedding-3-small", input=texts)
            for i, emb_obj in enumerate(response.data):
                new_chunks[i]["embedding"] = emb_obj.embedding
        _chunks = [c for c in new_chunks if c["embedding"]]
        _embeddings_ready = True
    except Exception as e:
        print(f"[RAG] Index build failed: {e}")
        _embeddings_ready = False

def _retrieve_context(query_embedding: List[float], top_k: int = 3) -> List[dict]:
    scored = []
    for chunk in _chunks:
        if chunk["embedding"]:
            score = cosine_similarity(query_embedding, chunk["embedding"])
            scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]

async def ask_coach(user_id: int, message: str, conversation_id: str, db: AsyncSession) -> str:
    if not settings.OPENAI_API_KEY:
        return _stub_response(message)
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        emb_response = await client.embeddings.create(model="text-embedding-3-small", input=[message])
        query_embedding = emb_response.data[0].embedding
        context_chunks = _retrieve_context(query_embedding)
        context_text = "\n\n".join(f"[{c['lesson_title']}]\n{c['text']}" for c in context_chunks)
        system_prompt = f"""You are FinPath Money Coach, a friendly UK financial literacy assistant for young adults aged 18-25.
Answer ONLY based on the lesson content provided below. If the answer is not in the content, say you don't have that information yet and suggest exploring the modules.
Keep responses concise, friendly, and use UK English.
NEVER give personal financial advice. Always stay educational.

LESSON CONTENT:
{context_text}"""
        chat_response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": message}],
            max_tokens=300,
            temperature=0.3,
        )
        answer = chat_response.choices[0].message.content or "I couldn't generate a response."
        log = AIChatLog(user_id=user_id, conversation_id=conversation_id, user_message=message[:1000], assistant_response=answer[:2000])
        db.add(log)
        await db.commit()
        return answer
    except Exception as e:
        print(f"[AI Coach] Error: {e}")
        return "I'm having trouble connecting right now. Please try again in a moment."

def _stub_response(message: str) -> str:
    msg = message.lower()
    if "credit score" in msg:
        return "A credit score in the UK is a number that lenders use to assess how reliably you repay debts. The higher your score, the more likely you are to be approved for credit at better rates."
    if "apr" in msg or "interest" in msg:
        return "APR stands for Annual Percentage Rate. It represents the true yearly cost of borrowing, including fees and interest. A lower APR means cheaper borrowing."
    if "ccj" in msg:
        return "A County Court Judgement (CCJ) is a court order issued if you fail to repay debts. It stays on your credit file for 6 years and makes it very difficult to get credit."
    return "Great question! Explore the learning modules to find detailed answers on that topic. I'm here to help clarify what you've learned in the lessons."
