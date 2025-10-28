import os
import json
import pickle
from build_index import MinimalVectorIndex


class SimpleIndexManager:
    """Простой менеджер для работы с индексом"""

    def __init__(self, index_path="vector_index_tfidf"):
        self.index_path = index_path
        self.index = None

    def load_index(self):
        """Загружает индекс"""
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index not found at {self.index_path}")

        self.index = MinimalVectorIndex()
        self.index.load_index(self.index_path)
        print(f"✓ Index loaded from {self.index_path}")
        return self.index

    def search(self, query, k=3):
        """Поиск в индексе"""
        if self.index is None:
            self.load_index()

        return self.index.search(query, k=k)

    def get_index_info(self):
        """Получает информацию об индексе"""
        metadata_path = os.path.join(self.index_path, "index_metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def interactive_search(self):
        """Интерактивный режим поиска"""
        self.load_index()

        print("=== INTERACTIVE SEARCH ===")
        print("Type 'quit' to exit")

        while True:
            query = input("\n🔍 Enter your question: ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                break

            if not query:
                continue

            print(f"Searching for: '{query}'")
            results = self.search(query, k=3)

            if results:
                for i, result in enumerate(results):
                    source = result['metadata']['filename']
                    score = result['score']
                    content = result['content']

                    print(f"\n📄 Result {i + 1} (score: {score:.3f}, source: {source}):")
                    print(f"   {content}")
            else:
                print("   No relevant results found.")


def demo():
    """Демонстрация работы"""
    manager = SimpleIndexManager()

    test_queries = [
        "Кто такой Zor Harris?",
        "Что такое Synth Flux?",
        "Опишите Annihilation Sphere",
        "Кто такие Aether Guardians?",
        "Какие корабли есть в галактике?"
    ]

    print("=== DEMONSTRATION ===")

    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = manager.search(query, k=2)

        for i, result in enumerate(results):
            source = result['metadata']['filename']
            score = result['score']
            content_preview = result['content'][:150] + "..." if len(result['content']) > 150 else result['content']
            print(f"   Result {i + 1} (score: {score:.3f}): {content_preview}")


if __name__ == "__main__":
    demo()
    # manager = SimpleIndexManager()
    # manager.interactive_search()