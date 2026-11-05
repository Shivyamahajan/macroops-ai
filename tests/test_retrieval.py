
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VECTOR_DB_DIR = PROJECT_ROOT / "data" / "vector_db"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
collection = client.get_collection("sop_knowledge")

questions = [
    "What should staff do when inventory discrepancy exceeds 10 units?",
    "What is the procedure for a product with a cracked seal?",
    "What should the team do when delivery riders are unavailable?",
    "What is the procedure for ordering a pizza?"
]

for question in questions:
    query_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        print(f"\nResult {i + 1}")
        print(f"Source: {metadata['source']}")
        print(f"Distance: {distance:.4f}")
        print(f"Content: {document[:250]}...")
