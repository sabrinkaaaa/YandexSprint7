import json
import os
import re
from faker import Faker
import random


class ImprovedTermReplacer:
    def __init__(self):
        self.faker = Faker()
        self.used_names = set()

    def generate_unique_name(self, base_type="character"):
        """Генерирует уникальное имя для замены"""
        if base_type == "character":
            templates = [
                f"{self.faker.first_name()} {self.faker.last_name()}",
                f"Xarn {self.faker.last_name()}",
                f"Kael {self.faker.last_name()}",
                f"Zor {self.faker.last_name()}"
            ]
        elif base_type == "planet":
            templates = [
                f"{self.faker.last_name()} Prime",
                f"New {self.faker.city()}",
                f"{self.faker.color_name()} {random.choice(['World', 'Planet', 'Sphere'])}",
                f"{self.faker.first_name()} {random.choice(['IV', 'V', 'VI', 'VII'])}"
            ]
        elif base_type == "technology":
            templates = [
                f"{self.faker.color_name()} {random.choice(['Core', 'Matrix', 'Engine', 'Drive'])}",
                f"Quantum {self.faker.last_name()}",
                f"{self.faker.first_name()} {random.choice(['Device', 'System', 'Technology'])}"
            ]
        else:
            templates = [f"{self.faker.word().capitalize()} {self.faker.word().capitalize()}"]

        name = random.choice(templates)
        while name in self.used_names:
            name = random.choice(templates)

        self.used_names.add(name)
        return name

    def create_comprehensive_replacement_map(self):
        """Создает полный словарь замены терминов"""
        replacement_map = {}

        # Расширенный словарь общих терминов
        general_terms = {
            # Основные концепции
            "The Force": "Synth Flux",
            "Force": "Flux",
            "force": "flux",
            "Dark Side": "Void Path",
            "dark side": "void path",
            "Light Side": "Luminous Path",
            "light side": "luminous path",

            # Организации
            "Jedi": "Aether Guardians",
            "jedi": "aether guardians",
            "Jedi Order": "Order of Aether",
            "Sith": "Void Bringers",
            "sith": "void bringers",
            "Rebel Alliance": "Nova Federation",
            "Rebel": "Nova",
            "rebel": "nova",
            "Galactic Empire": "Stellar Dominion",
            "Empire": "Dominion",
            "empire": "dominion",

            # Персонажи (добавим больше вариаций)
            "Luke Skywalker": "Zor Harris",
            "Luke": "Zor",
            "Darth Vader": "Xarn Clements",
            "Vader": "Clements",
            "Anakin Skywalker": "Kael Vossarian",
            "Anakin": "Kael",
            "Leia Organa": "Lyra Valerius",
            "Leia": "Lyra",
            "Han Solo": "Kael Dixon",
            "Han": "Kael",
            "Yoda": "Master Zenon",
            "Obi-Wan Kenobi": "Orin Valerius",
            "Obi-Wan": "Orin",
            "Chewbacca": "Grorg",
            "Chewie": "Grorg",
            "R2-D2": "AX-1",
            "C-3PO": "PX-0",
            "Lando Calrissian": "Silas Maridian",
            "Boba Fett": "Jax Korr",
            "Stormtrooper": "Dominion Trooper",
            "stormtrooper": "dominion trooper",
            "stormtroopers": "dominion troopers",

            # Планеты
            "Tatooine": "Kylos Prime",
            "Hoth": "Frigidia",
            "Endor": "Arborea",
            "Coruscant": "Aethelburg",
            "Naboo": "Cristina VI",

            # Технологии и корабли
            "Millennium Falcon": "Stardust Runner",
            "Falcon": "Runner",
            "Death Star": "Annihilation Sphere",
            "Lightsaber": "Plasma Blade",
            "lightsaber": "plasma blade",
            "lightsabers": "plasma blades",
            "Blaster": "Pulse Rifle",
            "blaster": "pulse rifle",
            "blasters": "pulse rifles",
            "Speeder Bike": "Grav-Cycle",
            "speeder bike": "grav-cycle",
            "speeder bikes": "grav-cycles",
            "AT-AT": "Titan Walker",
            "AT-ATs": "Titan Walkers",
            "Star Destroyer": "Void Cruiser",
            "star destroyer": "void cruiser",
            "star destroyers": "void cruisers",
            "X-wing": "Nova Interceptor",
            "X-wing": "nova interceptor",
            "X-wings": "nova interceptors",
            "TIE Fighter": "Dominion Fighter",
            "TIE fighter": "dominion fighter",
            "TIE fighters": "dominion fighters",

            # Расы и существа
            "Wookiee": "Ursian",
            "wookiee": "ursian",
            "Wookiees": "Ursians",
            "Ewok": "Arboreal",
            "ewok": "arboreal",
            "Ewoks": "Arboreals",
            "Droid": "Automaton",
            "droid": "automaton",
            "droids": "automatons",
            "Jabba the Hutt": "Vorlag the Magnificent",

            # События
            "Clone Wars": "Replication Conflict",
            "Battle of Yavin": "Siege of Aethel",
            "Battle of Hoth": "Battle of Frigidia"
        }

        replacement_map.update(general_terms)

        # Добавляем термины с разными регистрами
        additional_terms = {}
        for key, value in list(general_terms.items()):
            # Добавляем версии с заглавной буквой
            if key.lower() != key:
                additional_terms[key.lower()] = value.lower() if value.lower() != value else value
            # Добавляем версии с первой заглавной
            if key != key.title():
                additional_terms[key.title()] = value.title() if value.title() != value else value

        replacement_map.update(additional_terms)

        return replacement_map

    def replace_terms_in_text(self, text, replacement_map):
        """Заменяет термины в тексте с улучшенной логикой"""
        # Сортируем ключи по длине (от длинных к коротким)
        sorted_keys = sorted(replacement_map.keys(), key=len, reverse=True)

        for original in sorted_keys:
            # Используем regex для замены с учетом границ слов и регистра
            pattern = r'\b' + re.escape(original) + r'\b'
            try:
                text = re.sub(pattern, replacement_map[original], text, flags=re.IGNORECASE)
            except Exception as e:
                print(f"Warning: Error replacing '{original}': {e}")
                continue

        return text

    def process_all_documents(self, input_dir="knowledge_base/raw", output_dir="knowledge_base/processed_v2"):
        """Обрабатывает все документы с улучшенной логикой"""
        os.makedirs(output_dir, exist_ok=True)

        # Загружаем метаданные
        with open('knowledge_base/download_metadata.json', 'r', encoding='utf-8') as f:
            downloaded_pages = json.load(f)

        # Создаем полную карту замен
        replacement_map = self.create_comprehensive_replacement_map()

        processed_files = []

        for page_info in downloaded_pages:
            input_file = page_info['file']
            output_file = os.path.join(output_dir, os.path.basename(input_file))

            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Заменяем термины
                modified_content = self.replace_terms_in_text(content, replacement_map)

                # Дополнительная обработка для заголовков
                lines = modified_content.split('\n')
                if lines and lines[0].startswith('#'):
                    title = lines[0][1:].strip()
                    for original, replacement in replacement_map.items():
                        if original.lower() in title.lower():
                            title = re.sub(r'\b' + re.escape(original) + r'\b', replacement, title, flags=re.IGNORECASE)
                    lines[0] = f"# {title}"
                    modified_content = '\n'.join(lines)

                # Сохраняем обработанный файл
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(modified_content)

                processed_files.append({
                    'original_file': input_file,
                    'processed_file': output_file,
                    'original_title': page_info['title'],
                    'new_title': self.replace_terms_in_text(page_info['title'], replacement_map)
                })

                print(f"✓ Processed {os.path.basename(input_file)}")

            except Exception as e:
                print(f"✗ Error processing {input_file}: {e}")

        # Сохраняем полную карту замен
        with open('knowledge_base/terms_map_comprehensive.json', 'w', encoding='utf-8') as f:
            json.dump(replacement_map, f, indent=2, ensure_ascii=False)

        # Сохраняем метаданные обработки
        with open('knowledge_base/processing_metadata_v2.json', 'w', encoding='utf-8') as f:
            json.dump(processed_files, f, indent=2, ensure_ascii=False)

        print(f"\nProcessed {len(processed_files)} files")
        print(f"Replacement map contains {len(replacement_map)} terms")
        print("Comprehensive replacement map saved to knowledge_base/terms_map_comprehensive.json")

        return processed_files


def main():
    replacer = ImprovedTermReplacer()
    replacer.process_all_documents()


if __name__ == "__main__":
    main()