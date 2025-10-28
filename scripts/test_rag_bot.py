import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

from src.rag_bot import StandaloneRAGBot


def simple_test():
    print("=== ПРОСТОЙ ТЕСТ RAG БОТА ===\n")

    try:
        bot = StandaloneRAGBot()

        questions = [
            "Кто такой Zor Harris?",
            "Что такое Synth Flux?",
            "Какая столица Франции?",
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n{'=' * 50}")
            print(f"ТЕСТ {i}: {question}")
            print(f"{'=' * 50}")

            result = bot.process_question(question)

            print(f"ОТВЕТ (уверенность: {result['confidence']:.3f}):")
            print(result['answer'])

            if result['sources']:
                print(f"\nИсточники ({result['search_results_count']} найдено):")
                for source in result['sources']:
                    print(f"   - {source['filename']} (сходство: {source['score']:.3f})")

            if "не знаю" in result['answer'].lower():
                print("РЕЗУЛЬТАТ: Бот правильно говорит 'не знаю'")
            else:
                print("РЕЗУЛЬТАТ: Бот дает информативный ответ")

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    simple_test()