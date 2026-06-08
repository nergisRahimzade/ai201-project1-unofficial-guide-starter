import os
import re
import json

# --- Config ---
SOURCES_DIR = "sources"
OUTPUT_FILE = "documents/chunks.jsonl"
CHUNK_SIZE = 256
CHUNK_OVERLAP = 50

# --- Load ---
def load_documents(sources_dir):
    docs = []
    for root, dirs, files in os.walk(sources_dir):
        for filename in sorted(files):
            if not filename.endswith(".txt"):
                continue
            if filename.endswith("_url.txt"):  # skip URL files
                continue
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            # Look for sibling _url.txt in same folder
            url = None
            url_file = filepath.replace(".txt", "_url.txt")
            if os.path.exists(url_file):
                with open(url_file, "r", encoding="utf-8") as f:
                    url = f.read().strip()

            if text.strip():
                docs.append({
                    "source": filename,
                    "text": text,
                    "url": url
                })
    return docs

# --- Clean ---
def clean_text(text):
    text = re.sub(r"[ \t]{2,}", " ", text)    # collapse extra spaces
    text = re.sub(r"\n{3,}", "\n\n", text)    # collapse extra blank lines
    return text.strip()

# --- Chunk ---
def chunk_text(text, source, url, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    i = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({
                "id": f"{source}::chunk{i}",
                "text": chunk,
                "metadata": {
                    "source": source,
                    "url": url,
                    "chunk_index": i
                }
            })
            i += 1
        start += chunk_size - overlap
    return chunks

# --- Main ---
def main():
    docs = load_documents(SOURCES_DIR)
    print(f"Loaded {len(docs)} documents")

    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, doc["source"], doc["url"])
        all_chunks.extend(chunks)
        print(f"  {doc['source']}: {len(chunks)} chunks")

    os.makedirs("documents", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Saved to {OUTPUT_FILE}")

    # Verification — print 5 sample chunks
    print("\n--- 5 Sample Chunks ---")
    for chunk in all_chunks[:5]:
        print(f"\n[{chunk['id']}]")
        print(chunk["text"])
        print("-" * 40)

if __name__ == "__main__":
    main()