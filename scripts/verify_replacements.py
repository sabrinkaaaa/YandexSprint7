import json
import os
import re


def load_replacement_map():
    """Загружает карту замен"""
    with open('knowledge_base/terms_map_comprehensive.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def find_leaked_terms(text, replacement_map):
    """Находит утечки терминов в тексте"""
    leaked_terms = []

    # Создаем список всех оригинальных терминов для проверки
    original_terms = set(replacement_map.keys())

    # Добавляем базовые формы терминов (без окончаний)
    base_terms = set()
    for term in original_terms:
        # Убираем простые окончания
        base = re.sub(r'(s|es|ing|ed|er)$', '', term.lower())
        if len(base) > 3:  # Игнорируем слишком короткие базовые формы
            base_terms.add(base)

    for original in original_terms:
        # Ищем точные совпадения (с учетом регистра)
        if re.search(r'\b' + re.escape(original) + r'\b', text, re.IGNORECASE):
            leaked_terms.append(original)

    return leaked_terms


def verify_improved_replacements():
    """Проверяет качество замены терминов в улучшенной версии"""

    replacement_map = load_replacement_map()

    # Загружаем метаданные обработки
    with open('knowledge_base/processing_metadata_v2.json', 'r', encoding='utf-8') as f:
        processed_files = json.load(f)

    print("=== IMPROVED REPLACEMENT VERIFICATION ===")
    print(f"Total replacement terms: {len(replacement_map)}")
    print(f"Processed files: {len(processed_files)}")

    # Показываем несколько примеров замен
    print("\n=== SAMPLE REPLACEMENTS ===")
    import random
    sample_terms = random.sample(list(replacement_map.items()), 15)
    for original, replacement in sample_terms:
        print(f"  {original} → {replacement}")

    # Проверяем случайный файл
    if processed_files:
        sample_file = random.choice(processed_files)
        print(f"\n=== SAMPLE FILE: {sample_file['processed_file']} ===")

        with open(sample_file['processed_file'], 'r', encoding='utf-8') as f:
            content = f.read()

        # Показываем первые 500 символов
        preview = content[:500] + "..." if len(content) > 500 else content
        print(preview)

    # Детальная проверка утечек
    print("\n=== DETAILED LEAK CHECK ===")
    total_leaks = 0
    leak_details = {}

    for processed_file in processed_files:
        with open(processed_file['processed_file'], 'r', encoding='utf-8') as f:
            content = f.read()

        leaked_terms = find_leaked_terms(content, replacement_map)
        if leaked_terms:
            leak_details[processed_file['processed_file']] = leaked_terms
            total_leaks += len(leaked_terms)

    if leak_details:
        print(f"⚠️  Found {total_leaks} leaked terms across {len(leak_details)} files:")
        for filepath, terms in list(leak_details.items())[:10]:  # Показываем первые 10 файлов
            print(f"  {os.path.basename(filepath)}: {', '.join(terms[:5])}{'...' if len(terms) > 5 else ''}")

        if len(leak_details) > 10:
            print(f"  ... and {len(leak_details) - 10} more files with leaks")
    else:
        print("✓ No leaked terms found - excellent!")

    # Статистика
    print(f"\n=== STATISTICS ===")
    print(f"Total files checked: {len(processed_files)}")
    print(f"Files with leaks: {len(leak_details)}")
    print(f"Total leaked terms: {total_leaks}")

    return len(leak_details) == 0


if __name__ == "__main__":
    success = verify_improved_replacements()
    if success:
        print("\n🎉 SUCCESS! All terms properly replaced.")
    else:
        print("\n❌ Some terms still need fixing.")