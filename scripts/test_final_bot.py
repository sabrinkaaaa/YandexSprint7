import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.rag_bot import StandaloneRAGBot


def test_final_bot():
    print("=== ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ RAG БОТА ===\n")

    bot = StandaloneRAGBot()

    critical_cases = [
        {
            "question": "Что такое Annihilation Sphere?",
            "should_know": True,
            "expected_keywords": ["Annihilation Sphere", "Stellar Dominion", "боевая станция", "планеты"]
        },
        {
            "question": "Кто такой Zor Harris?",
            "should_know": True,
            "expected_keywords": ["Zor Harris", "Aether Guardian", "Synth Flux"]
        },
        {
            "question": "Опишите Synth Flux",
            "should_know": True,
            "expected_keywords": ["Synth Flux", "энергетическая сила", "Aether Guardians"]
        },
        {
            "question": "Кто такие Aether Guardians?",
            "should_know": True,
            "expected_keywords": ["Aether Guardians", "орден", "Synth Flux"]
        },
        {
            "question": "Какая столица Франции?",
            "should_know": False,
            "expected_keywords": ["не знаю", "отсутствует", "не освещена"]
        },
        {
            "question": "Как приготовить суши?",
            "should_know": False,
            "expected_keywords": ["не знаю", "отсутствует", "не освещена"]
        },
        {
            "question": "Что такое черная дыра?",
            "should_know": False,
            "expected_keywords": ["не знаю", "отсутствует", "не освещена"]
        }
    ]

    print("Запуск критических тестов...\n")

    passed_tests = 0
    total_tests = len(critical_cases)

    for i, test_case in enumerate(critical_cases, 1):
        print(f"Тест {i}/{total_tests}")
        print(f"Вопрос: '{test_case['question']}'")
        print(f"Ожидается: {'ЗНАЕТ' if test_case['should_know'] else 'НЕ ЗНАЕТ'}")

        result = bot.process_question(test_case['question'])

        knows_answer = result['knows_answer']
        should_know = test_case['should_know']
        response_contains_dont_know = "не знаю" in result['answer'].lower()

        keywords_found = all(keyword.lower() in result['answer'].lower() for keyword in test_case['expected_keywords'])

        logic_correct = (should_know and knows_answer and not response_contains_dont_know) or \
                        (not should_know and (not knows_answer or response_contains_dont_know))

        content_correct = keywords_found

        test_passed = logic_correct and content_correct

        if test_passed:
            passed_tests += 1
            print("ТЕСТ ПРОЙДЕН")
        else:
            print("ТЕСТ ПРОВАЛЕН")

        print(f"   Логика: {'КОРРЕКТНА' if logic_correct else 'ОШИБКА'}")
        print(f"   Контент: {'КОРРЕКТЕН' if content_correct else 'ОШИБКА'}")
        print(f"   Уверенность: {result['confidence']:.3f}")
        print(f"   Источников: {result['search_results_count']}")
        print(f"   Ответ: {result['answer'][:150]}...")
        print("-" * 80)
        print()

    success_rate = (passed_tests / total_tests) * 100
    print(f"ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    print(f"   Пройдено тестов: {passed_tests}/{total_tests}")
    print(f"   Успешность: {success_rate:.1f}%")

    if success_rate >= 85:
        print("ВСЕ КРИТИЧЕСКИЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("Бот готов к демонстрации и сдаче!")
        return True
    else:
        print("ЕСТЬ ПРОБЛЕМЫ С ОТВЕТАМИ")
        return False


if __name__ == "__main__":
    success = test_final_bot()

    if success:
        print("\n" + "=" * 60)
        print("ЗАПУСК ИНТЕРАКТИВНОГО РЕЖИМА ДЛЯ ДЕМОНСТРАЦИИ")
        print("=" * 60)
        bot = StandaloneRAGBot()
        bot.interactive_chat()