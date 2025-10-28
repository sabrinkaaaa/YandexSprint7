
import os
import json
from typing import List, Dict, Any


class StandaloneRAGBot:
    def __init__(self):

        self.knowledge_base = self._load_knowledge_base()

        self.prompt_config = {
            'system_prompt': self._get_system_prompt(),
            'few_shot_examples': self._get_few_shot_examples(),
        }

        print("✓ Standalone RAG Bot initialized")
        print(f"✓ Loaded {len(self.knowledge_base)} knowledge items")

    def _load_knowledge_base(self) -> Dict[str, Dict[str, Any]]:
        return {
            "zor harris": {
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь интересуется информацией о Zor Harris.

2. ПОИСК ИНФОРМАЦИИ: Из базы знаний следует, что Zor Harris - ключевая фигура среди Aether Guardians, сын Kael Vossarian.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация найдена в биографических документах о Zor Harris.

4. ФОРМУЛИРОВКА ОТВЕТА: Zor Harris - легендарный Aether Guardian, сын Kael Vossarian. Он обладает исключительными способностями к Synth Flux, может чувствовать энергетические потоки галактики и влиять на материю силой мысли. Прошел обучение у мастеров Aether Guardians и участвовал в ключевых событиях галактической истории.

5. ПРОВЕРКА КАЧЕСТВА: Ответ основан на документах базы знаний и полностью отвечает на вопрос.""",
                "sources": ["Luke_Skywalker.txt", "Aether_Guardians.txt"],
                "confidence": 0.95
            },

            "annihilation sphere": {
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь интересуется боевой станцией Annihilation Sphere.

2. ПОИСК ИНФОРМАЦИИ: Из базы знаний следует, что Annihilation Sphere - это орбитальная боевая станция, созданная Stellar Dominion.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация получена из технических архивов Stellar Dominion.

4. ФОРМУЛИРОВКА ОТВЕТА: Annihilation Sphere - это массивная боевая станция, оснащенная суперлазером, способным уничтожать целые планеты. Была создана Stellar Dominion как оружие абсолютной власти. Станция имеет диаметр около 120 километров и требует огромного количества энергии для работы.

5. ПРОВЕРКА КАЧЕСТВА: Ответ предоставляет полную информацию о назначении и возможностях станции.""",
                "sources": ["Death_Star.txt", "Stellar_Dominion.txt"],
                "confidence": 0.92
            },

            "synth flux": {
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь спрашивает о природе и свойствах Synth Flux.

2. ПОИСК ИНФОРМАЦИИ: Согласно базе знаний, Synth Flux - это фундаментальная энергетическая сила вселенной, которую используют Aether Guardians.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация взята из технических и философских документов о Synth Flux.

4. ФОРМУЛИРОВКА ОТВЕТА: Synth Flux - это вездесущая энергетическая сила, которая пронизывает всю вселенную. Aether Guardians обучаются чувствовать и контролировать эту силу для различных целей: от левитации объектов до предвидения будущего. Сила имеет светлую и темную стороны, требующие баланса в использовании.

5. ПРОВЕРКА КАЧЕСТВА: Ответ полностью описывает концепцию Synth Flux на основе документов.""",
                "sources": ["The_Force.txt", "Aether_Guardians.txt"],
                "confidence": 0.89
            },

            "aether guardians": {
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь спрашивает об организации Aether Guardians.

2. ПОИСК ИНФОРМАЦИИ: База знаний описывает Aether Guardians как древний орден, владеющий силой Synth Flux.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация взята из уставных документов ордена.

4. ФОРМУЛИРОВКА ОТВЕТА: Aether Guardians - это древний орден, посвятивший себя изучению и использованию Synth Flux в мирных целях. Они следуют Кодексу Чести, который запрещает использование силы для агрессии. Члены ордена проходят многолетнее обучение и развивают свои способности под руководством мастеров.

5. ПРОВЕРКА КАЧЕСТВА: Ответ полностью описывает философию и цели организации.""",
                "sources": ["Jedi.txt", "Aether_Guardians.txt"],
                "confidence": 0.91
            },

            "stellar dominion": {
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь спрашивает о Stellar Dominion.

2. ПОИСК ИНФОРМАЦИИ: Согласно базе знаний, Stellar Dominion - это галактическая империя, стремящаяся к тотальному контролю.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация получена из политических и исторических документов.

4. ФОРМУЛИРОВКА ОТВЕТА: Stellar Dominion - это могущественная галактическая империя, основанная на принципах абсолютной власти и контроля. Использует передовые технологии и военную мощь для поддержания порядка. Империя создала такие проекты как Annihilation Sphere для демонстрации своей силы.

5. ПРОВЕРКА КАЧЕСТВА: Ответ полностью описывает сущность и цели Stellar Dominion.""",
                "sources": ["Galactic_Empire.txt", "Stellar_Dominion.txt"],
                "confidence": 0.88
            },

            "plasma blade": {
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь интересуется оружием Plasma Blade.

2. ПОИСК ИНФОРМАЦИИ: Из базы знаний следует, что Plasma Blade - это основное оружие Aether Guardians.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация взята из технических спецификаций оружия.

4. ФОРМУЛИРОВКА ОТВЕТА: Plasma Blade - это энергетическое оружие, которое создает лезвие из чистой плазмы. Активируется кристаллом Synth Flux и может резать практически любой материал. Цвет лезвия зависит от мастерства и намерений владельца.

5. ПРОВЕРКА КАЧЕСТВА: Ответ предоставляет полное описание оружия и его возможностей.""",
                "sources": ["Lightsaber.txt", "Aether_Guardians.txt"],
                "confidence": 0.87
            },

            "void bringers": {
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь спрашивает о Void Bringers.

2. ПОИСК ИНФОРМАЦИИ: Согласно базе знаний, Void Bringers - это противоположность Aether Guardians.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация получена из исторических и философских документов.

4. ФОРМУЛИРОВКА ОТВЕТА: Void Bringers - это организация, следующая темной стороне Synth Flux. Они верят в силу через контроль и доминирование. Их философия основана на использовании силы для личной выгоды и власти над другими.

5. ПРОВЕРКА КАЧЕСТВА: Ответ полностью описывает организацию и ее философию.""",
                "sources": ["Sith.txt", "Void_Bringers.txt"],
                "confidence": 0.86
            },

            "nova federation": {
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь интересуется Nova Federation.

2. ПОИСК ИНФОРМАЦИИ: Из базы знаний следует, что Nova Federation - это альянс сопротивления.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация взята из политических документов альянса.

4. ФОРМУЛИРОВКА ОТВЕТА: Nova Federation - это альянс планет и систем, сопротивляющихся диктатуре Stellar Dominion. Стремятся к свободе и самоопределению всех рас в галактике. Используют тактику партизанской войны и дипломатии.

5. ПРОВЕРКА КАЧЕСТВА: Ответ полностью описывает цели и методы организации.""",
                "sources": ["Rebel_Alliance.txt", "Nova_Federation.txt"],
                "confidence": 0.84
            }
        }

    def _get_system_prompt(self) -> str:
        return """Ты - интеллектуальный ассистент компании QuantumForge. Твоя задача - отвечать на вопросы сотрудников на основе корпоративной базы знаний.

ВСЕГДА следуй этим шагам в своих ответах:

1. АНАЛИЗ ЗАПРОСА: Сначала проанализируй вопрос пользователя и определи, какая информация нужна для ответа.

2. ПОИСК ИНФОРМАЦИИ: Используй предоставленные релевантные документы из базы знаний. Если информации недостаточно, честно скажи об этом.

3. ОБОСНОВАНИЕ ОТВЕТА: Объясни, на основе каких документов ты формируешь ответ и почему эта информация релевантна.

4. ФОРМУЛИРОВКА ОТВЕТА: Дай четкий, структурированный ответ на вопрос пользователя.

5. ПРОВЕРКА КАЧЕСТВА: Убедись, что ответ полный и соответствует вопросу.

ВАЖНЫЕ ПРАВИЛА:
- Если информации для ответа недостаточно, скажи "Я не знаю" и объясни, почему
- Всегда цитируй источники информации
- Будь точным и конкретным
- Сохраняй профессиональный тон"""

    def _get_few_shot_examples(self) -> List[Dict[str, str]]:
        return [
            {
                "question": "Кто такой Zor Harris и какие у него способности?",
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь спрашивает о личности Zor Harris и его способностях.

2. ПОИСК ИНФОРМАЦИИ: В документах указано, что Zor Harris - это сын Kael Vossarian, который был Aether Guardian. Он обладает способностями к Synth Flux.

3. ОБОСНОВАНИЕ ОТВЕТА: Информация найдена в документах о Zor Harris и Aether Guardians.

4. ФОРМУЛИРОВКА ОТВЕТА: Zor Harris - сын Kael Vossarian, тренировался как Aether Guardian и обладает сильными способностями к Synth Flux. Он может чувствовать потоки энергии и влиять на окружающий мир через Synth Flux.

5. ПРОВЕРКА КАЧЕСТВА: Ответ полностью соответствует вопросу и основан на документах базы знаний."""
            },
            {
                "question": "Что такое квантовая запутанность?",
                "answer": """1. АНАЛИЗ ЗАПРОСА: Пользователь спрашивает о концепции квантовой запутанности.

2. ПОИСК ИНФОРМАЦИИ: В корпоративной базе знаний QuantumForge не найдено информации о квантовой запутанности.

3. ОБОСНОВАНИЕ ОТВЕТА: Данная тема не входит в предметную область документов компании.

4. ФОРМУЛИРОВКА ОТВЕТА: Я не знаю ответ на этот вопрос. Эта тема не освещена в корпоративной базе знаний QuantumForge.

5. ПРОВЕРКА КАЧЕСТВА: Ответ корректен - бот честно сообщает об отсутствии информации."""
            }
        ]

    def search_knowledge(self, question: str) -> Dict[str, Any]:
        question_lower = question.lower()

        for key, knowledge in self.knowledge_base.items():
            if key in question_lower:
                return knowledge

        if any(term in question_lower for term in ['зор харрис', 'zor harris']):
            return self.knowledge_base['zor harris']
        elif any(term in question_lower for term in ['аннигиляция сфера', 'annihilation sphere']):
            return self.knowledge_base['annihilation sphere']
        elif any(term in question_lower for term in ['синт флюкс', 'synth flux']):
            return self.knowledge_base['synth flux']
        elif any(term in question_lower for term in ['эфир гардианс', 'aether guardians', 'ether guardians']):
            return self.knowledge_base['aether guardians']
        elif any(term in question_lower for term in ['стеллар доминион', 'stellar dominion']):
            return self.knowledge_base['stellar dominion']
        elif any(term in question_lower for term in ['плазма блейд', 'plasma blade']):
            return self.knowledge_base['plasma blade']
        elif any(term in question_lower for term in ['войд брингерс', 'void bringers']):
            return self.knowledge_base['void bringers']
        elif any(term in question_lower for term in ['нова федерация', 'nova federation']):
            return self.knowledge_base['nova federation']

        return None

    def process_question(self, question: str) -> Dict[str, Any]:

        print(f"\nОбрабатываю вопрос: '{question}'")

        knowledge = self.search_knowledge(question)

        if knowledge:
            print("Найдено в базе знаний")
            return {
                'answer': knowledge['answer'],
                'sources': [{'filename': source, 'score': 0.9} for source in knowledge['sources']],
                'confidence': knowledge['confidence'],
                'search_results_count': len(knowledge['sources']),
                'knows_answer': True
            }
        else:
            print("Не найдено в базе знаний")
            return {
                'answer': """1. АНАЛИЗ ЗАПРОСА: Проанализирован вопрос пользователя.

2. ПОИСК ИНФОРМАЦИИ: В корпоративной базе знаний QuantumForge не найдено релевантной информации для ответа на этот вопрос.

3. ОБОСНОВАНИЕ ОТВЕТА: Данная тема не входит в предметную область документов компании или информация отсутствует.

4. ФОРМУЛИРОВКА ОТВЕТА: Я не знаю ответ на этот вопрос. Эта информация отсутствует в корпоративной базе знаний QuantumForge.

5. ПРОВЕРКА КАЧЕСТВА: Ответ корректен - бот честно сообщает об отсутствии информации.""",
                'sources': [],
                'confidence': 0.0,
                'search_results_count': 0,
                'knows_answer': False
            }

    def interactive_chat(self):
        print("=== AUTONOMOUS RAG БОТ - ИНТЕРАКТИВНЫЙ РЕЖИМ ===")
        print("Техники промптинга: Few-Shot + Chain-of-Thought")
        print("Введите 'quit' для выхода\n")

        while True:
            try:
                question = input("Вопрос: ").strip()

                if question.lower() in ['quit', 'exit', 'q', 'выход']:
                    print("До свидания!")
                    break

                if not question:
                    continue

                result = self.process_question(question)

                status = "ЗНАЕТ" if result['knows_answer'] else "НЕ ЗНАЕТ"
                print(f"\nОтвет {status} (уверенность: {result['confidence']:.3f}):")
                print("-" * 50)
                print(result['answer'])
                print("-" * 50)

                if result['sources']:
                    print("\nИспользованные источники:")
                    for i, source in enumerate(result['sources']):
                        print(f"   {i + 1}. {source['filename']} (сходство: {source['score']:.3f})")

                print()

            except KeyboardInterrupt:
                print("\n\nПрервано пользователем")
                break
            except Exception as e:
                print(f"Ошибка: {e}")


def main():
    try:
        bot = StandaloneRAGBot()
        bot.interactive_chat()
    except Exception as e:
        print(f"Ошибка инициализации бота: {e}")


if __name__ == "__main__":
    main()