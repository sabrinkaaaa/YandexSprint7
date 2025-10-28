import os
from dotenv import load_dotenv

load_dotenv()

# Конфигурация RAG бота
RAG_CONFIG = {
    'index_path': 'vector_index_tfidf',
    'max_search_results': 3,
    'min_confidence': 0.1,
    'chunk_size': 500
}

# Конфигурация промптинга
PROMPT_CONFIG = {
    'system_prompt': """
Ты - ассистент QuantumForge. Отвечай точно на основе документов.
Всегда используй Chain-of-Thought:
1. Анализ вопроса
2. Поиск в документах  
3. Обоснование ответа
4. Формулировка ответа
5. Проверка качества
""",
    'enable_few_shot': True,
    'enable_cot': True
}

# API конфигурация (если будем использовать реальные LLM)
API_CONFIG = {
    'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
    'yandex_gpt_api_key': os.getenv('YANDEX_GPT_API_KEY', ''),
    'use_local_fallback': True
}