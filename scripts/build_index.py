import os
import json
import glob
import time
from datetime import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


class MinimalVectorIndex:
    def __init__(self):
        self.vectorizer = None
        self.documents = []
        self.embeddings = None
        self.metadata = []

    def load_documents(self, docs_dir="knowledge_base/processed_v2"):
        """Загружает документы из директории"""
        print(f"Loading documents from: {docs_dir}")

        if not os.path.exists(docs_dir):
            raise FileNotFoundError(f"Directory {docs_dir} not found")

        documents = []
        txt_files = glob.glob(os.path.join(docs_dir, "*.txt"))

        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                filename = os.path.basename(file_path)
                documents.append(content)
                self.metadata.append({
                    'filename': filename,
                    'source': file_path,
                    'doc_id': filename.replace('.txt', '')
                })
                print(f"  Loaded: {filename}")

            except Exception as e:
                print(f"  Error loading {file_path}: {e}")

        print(f"✓ Loaded {len(documents)} documents")
        return documents

    def split_into_chunks(self, documents, chunk_size=500, chunk_overlap=50):
        """Разбивает документы на чанки"""
        print(f"Splitting into chunks (size: {chunk_size}, overlap: {chunk_overlap})")

        chunks = []
        chunk_metadata = []

        for doc_content, meta in zip(documents, self.metadata):
            words = doc_content.split()

            # Простое разбиение по словам
            for i in range(0, len(words), chunk_size - chunk_overlap):
                chunk_words = words[i:i + chunk_size]
                if len(chunk_words) < 100:  # Пропускаем слишком короткие чанки
                    continue

                chunk_text = ' '.join(chunk_words)
                chunks.append(chunk_text)
                chunk_metadata.append({
                    'filename': meta['filename'],
                    'source': meta['source'],
                    'chunk_id': f"{meta['doc_id']}_chunk_{i}",
                    'word_count': len(chunk_words)
                })

        print(f"✓ Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks, chunk_metadata

    def build_tfidf_index(self, chunks, chunk_metadata):
        """Строит TF-IDF индекс"""
        print("Building TF-IDF index...")

        start_time = time.time()

        # Создаем TF-IDF векторайзер
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            min_df=1,
            max_df=0.8,
            stop_words='english'
        )

        # Создаем TF-IDF матрицу
        self.embeddings = self.vectorizer.fit_transform(chunks)
        self.documents = chunks
        self.metadata = chunk_metadata

        end_time = time.time()
        build_time = end_time - start_time

        print(f"✓ TF-IDF index built with {self.embeddings.shape[1]} features")
        print(f"Indexing time: {build_time:.2f} seconds")

        return self.embeddings

    def search(self, query, k=3):
        """Поиск по индексу"""
        if self.vectorizer is None or self.embeddings is None:
            raise ValueError("Index not built yet")

        # Преобразуем запрос в TF-IDF вектор
        query_vec = self.vectorizer.transform([query])

        # Вычисляем косинусное сходство
        similarities = cosine_similarity(query_vec, self.embeddings).flatten()

        # Получаем топ-K результатов
        top_indices = similarities.argsort()[-k:][::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Минимальный порог сходства
                results.append({
                    'content': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'score': similarities[idx]
                })

        return results

    def save_index(self, index_path="vector_index"):
        """Сохраняет индекс на диск"""
        print(f"Saving index to: {index_path}")

        os.makedirs(index_path, exist_ok=True)

        # Сохраняем компоненты индекса
        with open(os.path.join(index_path, "vectorizer.pkl"), 'wb') as f:
            pickle.dump(self.vectorizer, f)

        with open(os.path.join(index_path, "embeddings.pkl"), 'wb') as f:
            pickle.dump(self.embeddings, f)

        with open(os.path.join(index_path, "documents.json"), 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)

        with open(os.path.join(index_path, "metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

        # Сохраняем метаданные индекса
        index_metadata = {
            'build_time': datetime.now().isoformat(),
            'embedding_type': 'TF-IDF',
            'total_chunks': len(self.documents),
            'vocabulary_size': self.embeddings.shape[1],
            'chunk_size_stats': {
                'min': min(len(doc.split()) for doc in self.documents) if self.documents else 0,
                'max': max(len(doc.split()) for doc in self.documents) if self.documents else 0,
                'avg': sum(len(doc.split()) for doc in self.documents) / len(self.documents) if self.documents else 0
            },
            'sources': list(set(meta['filename'] for meta in self.metadata))
        }

        with open(os.path.join(index_path, "index_metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(index_metadata, f, ensure_ascii=False, indent=2)

        print(f"✓ Index saved to {index_path}")
        return index_metadata

    def load_index(self, index_path="vector_index"):
        """Загружает индекс с диска"""
        print(f"Loading index from: {index_path}")

        with open(os.path.join(index_path, "vectorizer.pkl"), 'rb') as f:
            self.vectorizer = pickle.load(f)

        with open(os.path.join(index_path, "embeddings.pkl"), 'rb') as f:
            self.embeddings = pickle.load(f)

        with open(os.path.join(index_path, "documents.json"), 'r', encoding='utf-8') as f:
            self.documents = json.load(f)

        with open(os.path.join(index_path, "metadata.json"), 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)

        print(f"✓ Index loaded with {len(self.documents)} chunks")
        return True


def test_search(index):
    """Тестирует поиск по индексу"""
    test_queries = [
        "Кто такой Zor Harris?",
        "Что такое Synth Flux?",
        "Опишите Annihilation Sphere",
        "Какие корабли использует Stellar Dominion?",
        "Кто такие Aether Guardians?"
    ]

    print("\n=== TESTING SEARCH ===")

    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = index.search(query, k=2)

        for i, result in enumerate(results):
            source = result['metadata']['filename']
            score = result['score']
            content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
            print(f"   Result {i + 1} (score: {score:.3f}, source: {source}):")
            print(f"   {content_preview}")


def main():
    """Основная функция построения индекса"""

    # Конфигурация
    CONFIG = {
        'docs_directory': 'knowledge_base/processed_v2',
        'index_path': 'vector_index_tfidf',
        'chunk_size': 500,
        'chunk_overlap': 50
    }

    print("=== BUILDING MINIMAL VECTOR INDEX ===")
    print(f"Configuration: {CONFIG}")

    try:
        # Инициализация индекса
        index = MinimalVectorIndex()

        # Шаг 1: Загрузка документов
        documents = index.load_documents(CONFIG['docs_directory'])

        # Шаг 2: Разбиение на чанки
        chunks, chunk_metadata = index.split_into_chunks(
            documents,
            chunk_size=CONFIG['chunk_size'],
            chunk_overlap=CONFIG['chunk_overlap']
        )

        # Шаг 3: Построение индекса
        index.build_tfidf_index(chunks, chunk_metadata)

        # Шаг 4: Сохранение индекса
        metadata = index.save_index(CONFIG['index_path'])

        # Шаг 5: Тестирование поиска
        test_search(index)

        # Финальная статистика
        print(f"\n=== INDEX BUILD COMPLETE ===")
        print(f"Total documents: {len(documents)}")
        print(f"Total chunks: {len(chunks)}")
        print(f"Vocabulary size: {index.embeddings.shape[1]}")
        print(f"Index saved to: {CONFIG['index_path']}")

        return {
            'success': True,
            'index': index,
            'metadata': metadata
        }

    except Exception as e:
        print(f"❌ Error building index: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    result = main()