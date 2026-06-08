import os
import json

from sentence_transformers import SentenceTransformer
import chromadb

# --- Config ---
CHUNKS_FILE = "documents/chunks.jsonl"
CHROMA_DIR = "documents/chroma_db"
COLLECTION_NAME = "stanford_dining"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5

_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


# --- Load chunks ---
def load_chunks(chunks_file=CHUNKS_FILE):
    chunks = []
    with open(chunks_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


# --- Embed + store ---
def build_vector_store(chunks, chroma_dir=CHROMA_DIR, collection_name=COLLECTION_NAME):
    model = get_model()

    ids = [c["id"] for c in chunks]
    texts = [c["text"] for c in chunks]

    metadatas = []
    for c in chunks:
        meta = c["metadata"]
        metadatas.append({
            "source": meta["source"],
            "url": meta.get("url") or "",
            "chunk_index": meta["chunk_index"],
        })

    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    client = chromadb.PersistentClient(path=chroma_dir)
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return collection


def get_collection(chroma_dir=CHROMA_DIR, collection_name=COLLECTION_NAME):
    client = chromadb.PersistentClient(path=chroma_dir)
    return client.get_collection(collection_name)


# --- Retrieve ---
def retrieve(query, top_k=TOP_K, collection=None):
    if collection is None:
        collection = get_collection()

    model = get_model()
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    hits = []
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]
    for text, meta, dist in zip(docs, metas, dists):
        hits.append({
            "text": text,
            "source": meta.get("source"),
            "url": meta.get("url"),
            "chunk_index": meta.get("chunk_index"),
            "distance": dist,
        })
    return hits


# --- Main ---
def main():
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE}")

    collection = build_vector_store(chunks)
    print(f"Stored {collection.count()} chunks in ChromaDB at {CHROMA_DIR}")
    print(f"Collection: {COLLECTION_NAME} | model: {MODEL_NAME} | top-k: {TOP_K}")

    sample_query = "Which dining hall has the best Indian food?"
    print(f"\n--- Sample retrieval ---\nQuery: {sample_query}\n")
    for i, hit in enumerate(retrieve(sample_query, collection=collection), 1):
        preview = hit["text"][:160].replace("\n", " ")
        print(f"{i}. [{hit['source']}#chunk{hit['chunk_index']}] (distance={hit['distance']:.4f})")
        print(f"   {preview}...")
        print("-" * 40)


if __name__ == "__main__":
    main()
