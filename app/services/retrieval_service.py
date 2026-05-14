from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global storage
document_chunks = []
index = None


def create_vector_store(chunks):
    global document_chunks, index

    document_chunks = chunks

    # Convert text chunks to embeddings
    embeddings = model.encode(chunks)

    # Convert to FAISS-compatible format
    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings
    index.add(embeddings)

    return len(chunks)


def search_similar_chunks(query, top_k=3):
    global index, document_chunks

    if index is None:
        return []

    # Query embedding
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Search
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(document_chunks):
            results.append(document_chunks[idx])

    return results