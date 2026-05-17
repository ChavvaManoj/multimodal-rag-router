from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import json

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Storage paths
FAISS_INDEX_PATH = "data/faiss_index.bin"
METADATA_PATH = "data/document_metadata.json"

# Global storage
document_chunks = []
chunk_sources = []
index = None


def save_vector_store():
    global index, document_chunks, chunk_sources

    os.makedirs("data", exist_ok=True)

    # Save FAISS index
    if index is not None:
        faiss.write_index(index, FAISS_INDEX_PATH)

    # Save metadata
    metadata = {
        "document_chunks": document_chunks,
        "chunk_sources": chunk_sources
    }

    with open(METADATA_PATH, "w") as file:
        json.dump(metadata, file)


def load_vector_store():
    global index, document_chunks, chunk_sources

    # Load FAISS index
    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)

    # Load metadata
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as file:
            metadata = json.load(file)

            document_chunks = metadata.get("document_chunks", [])
            chunk_sources = metadata.get("chunk_sources", [])


def create_vector_store(chunks, source_name):
    global document_chunks, chunk_sources, index

    # Load existing data first
    load_vector_store()

    # Append new chunks
    document_chunks.extend(chunks)
    chunk_sources.extend([source_name] * len(chunks))

    # Generate embeddings
    embeddings = model.encode(document_chunks)
    embeddings = np.array(embeddings).astype("float32")

    # Rebuild index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save updated store
    save_vector_store()

    return len(chunks)


def search_similar_chunks(query, top_k=3):
    global index, document_chunks, chunk_sources

    # Load store before searching
    load_vector_store()

    if index is None:
        return []

    # Detect source preference
    query_lower = query.lower()

    preferred_media = None

    if "video" in query_lower:
        preferred_media = [".mp4"]
    elif "audio" in query_lower or "recording" in query_lower:
        preferred_media = [".mp3", ".wav", ".m4a"]

    # Query embedding
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Search larger pool first
    search_pool = max(top_k * 5, 10)

    distances, indices = index.search(query_embedding, search_pool)

    results = []

    for idx in indices[0]:
        if idx >= len(document_chunks):
            continue

        source = chunk_sources[idx]

        # Media-aware filtering
        if preferred_media:
            if not any(source.lower().endswith(ext) for ext in preferred_media):
                continue

        results.append({
            "source": source,
            "content": document_chunks[idx]
        })

        if len(results) >= top_k:
            break

    # Fallback if no preferred media found
    if not results:
        for idx in indices[0][:top_k]:
            if idx < len(document_chunks):
                results.append({
                    "source": chunk_sources[idx],
                    "content": document_chunks[idx]
                })

    return results