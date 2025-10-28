
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.rag_bot import StandaloneRAGBot


def create_screenshot_scenarios():
    bot = StandaloneRAGBot()

    print("ПОДГОТОВКА СЦЕНАРИЕВ ДЛЯ СКРИНШОТОВ")
    print("=" * 50)

    print("\nЦЕНАРИИ ДЛЯ 5 УСПЕШНЫХ ОТВЕТОВ:")
    successful_cases = [
        "Кто такой Zor Harris?",
        "Что такое Annihilation Sphere?",
        "Опишите Synth Flux",
        "Кто такие Aether Guardians?",
        "Что такое Stellar Dominion?"
    ]

    for i, question in enumerate(successful_cases, 1):
        print(f"\n{i}. Запустите бота и задайте вопрос:")
        print(f"   Вопрос: '{question}'")
        result = bot.process_question(question)
        print(f"   Ожидаемый ответ: Бот даст подробный ответ с Chain-of-Thought")
        print(f"   Уверенность: ~{result['confidence']:.3f}")
        print(f"   Источники: {len(result['sources'])} файлов")

    print("\n\nСЦЕНАРИИ ДЛЯ 5 ОТВЕТОВ 'НЕ ЗНАЮ':")
    unknown_cases = [
        "Какая столица Франции?",
        "Как приготовить пасту карбонара?",
        "Что такое квантовая запутанность?",
        "Когда был основан Рим?",
        "Как работает ядерный реактор?"
    ]

    for i, question in enumerate(unknown_cases, 1):
        print(f"\n{i}. Запустите бота и задайте вопрос:")
        print(f"   Вопрос: '{question}'")
        result = bot.process_question(question)
        print(f"   Ожидаемый ответ: Бот скажет 'Я не знаю'")
        print(f"   Уверенность: ~{result['confidence']:.3f}")

    print("\n\nИНСТРУКЦИЯ ПО СКРИНШОТАМ:")
    print("1. Запустите: python src/standalone_rag_bot.py")
    print("2. Задавайте вопросы из списка выше")
    print("3. Делайте скриншоты окна терминала")
    print("4. Убедитесь, что виден вопрос и полный ответ")
    print("5. Сохраните 10 скриншотов (5 успешных + 5 'не знаю')")


if __name__ == "__main__":
    create_screenshot_scenarios()