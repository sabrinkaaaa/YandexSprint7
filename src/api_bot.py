from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_bot import RAGBot
import uvicorn

app = FastAPI(
    title="QuantumForge RAG Bot API",
    description="Интеллектуальный бот для поиска в корпоративной базе знаний",
    version="1.0.0"
)

# Инициализация бота
bot = None


class QuestionRequest(BaseModel):
    question: str
    max_results: int = 3


class BotResponse(BaseModel):
    answer: str
    sources: list
    confidence: float
    search_results_count: int


@app.on_event("startup")
async def startup_event():
    """Инициализация бота при запуске"""
    global bot
    try:
        bot = RAGBot()
        print("✓ RAG Bot API started successfully")
    except Exception as e:
        print(f"❌ Failed to initialize bot: {e}")


@app.get("/")
async def root():
    return {"message": "QuantumForge RAG Bot API", "status": "running"}


@app.post("/ask", response_model=BotResponse)
async def ask_question(request: QuestionRequest):
    """Обработка вопроса пользователя"""
    if bot is None:
        raise HTTPException(status_code=500, detail="Bot not initialized")

    try:
        result = bot.process_question(request.question)
        return BotResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "bot_initialized": bot is not None}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)