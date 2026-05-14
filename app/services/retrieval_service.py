from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global storage
document_chunks = []
chunk_sources = []
index = None


def create_vector_store(chunks, source_name):
    global document_chunks, chunk_sources, index

    # Append instead of overwrite
    document_chunks.extend(chunks)
    chunk_sources.extend([source_name] * len(chunks))

    # Generate embeddings for ALL chunks
    embeddings = model.encode(document_chunks)
    embeddings = np.array(embeddings).astype("float32")

    # Rebuild FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return len(chunks)


def search_similar_chunks(query, top_k=3):
    global index, document_chunks, chunk_sources

    if index is None:
        return []

    # Query embedding
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(document_chunks):
            results.append({
                "source": chunk_sources[idx],
                "content": document_chunks[idx]
            })

    return results