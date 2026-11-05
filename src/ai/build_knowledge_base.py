
"""
MacroOps AI - SOP Knowledge Base Builder

Reads operational SOP documents, creates text chunks,
generates embeddings, and stores them in ChromaDB.
"""

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"
VECTOR_DB_DIR = PROJECT_ROOT / "data" / "vector_db"

# Model and collection settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "sop_knowledge"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping character-based chunks."""

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def main():
    print("\n=== MacroOps AI Knowledge Base Builder ===\n")

    # Find SOP documents
    files = sorted(KNOWLEDGE_BASE_DIR.glob("*.txt"))

    if not files:
        print("ERROR: No .txt documents found.")
        return

    print(f"Found {len(files)} knowledge-base documents.")

    # Load embedding model
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    documents = []
    metadatas = []
    ids = []

    # Read and split documents
    for file_path in files:
        text = file_path.read_text(encoding="utf-8")
        chunks = split_text(text)

        for index, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "source": file_path.name,
                "chunk_index": index,
                "title": file_path.stem.replace("_", " ").title()
            })
            ids.append(f"{file_path.stem}_{index}")

        print(f"  {file_path.name}: {len(chunks)} chunks")

    print(f"\nTotal chunks created: {len(documents)}")

    # Generate embeddings
    print("\nGenerating embeddings...")
    embeddings = model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    # Create persistent ChromaDB client
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

    # Rebuild collection for a fresh, reproducible index
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    # Store documents and embeddings
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print("\n=== Knowledge Base Build Complete ===")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Documents: {len(files)}")
    print(f"Chunks stored: {collection.count()}")
    print(f"Vector database: {VECTOR_DB_DIR}")


if __name__ == "__main__":
    main()
