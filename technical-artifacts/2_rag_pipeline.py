"""
RAG Pipeline — Reference Implementation
-----------------------------------------
Demonstrates the core stages of Retrieval-Augmented Generation:
chunk -> embed -> store -> retrieve -> inject into prompt -> generate.

This mirrors what Amazon Bedrock Knowledge Bases does under the hood,
implemented manually here to show understanding of each step rather
than treating the managed service as a black box.

Domain: Foundation Models, Data & RAG
"""

import boto3
import json
import numpy as np

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"
GEN_MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"


# ---------- 1. Chunking ----------
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Splits a document into overlapping chunks.
    Overlap matters because a fact that gets cut off at a chunk boundary
    would otherwise be lost or garbled when retrieved on its own.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# ---------- 2. Embedding ----------
def embed_text(text: str):
    """Converts a chunk of text into a vector using a Bedrock embedding model."""
    body = json.dumps({"inputText": text})
    response = bedrock.invoke_model(modelId=EMBED_MODEL_ID, body=body)
    result = json.loads(response["body"].read())
    return np.array(result["embedding"])


# ---------- 3. In-memory vector store ----------
class SimpleVectorStore:
    """
    A minimal stand-in for what a managed vector store (OpenSearch Serverless,
    Pinecone, etc.) does: stores (chunk, vector) pairs and finds the closest
    matches to a query vector using cosine similarity.
    """

    def __init__(self):
        self.chunks = []
        self.vectors = []

    def add(self, chunk: str, vector: np.ndarray):
        self.chunks.append(chunk)
        self.vectors.append(vector)

    def search(self, query_vector: np.ndarray, top_k: int = 3):
        sims = [
            np.dot(query_vector, v) / (np.linalg.norm(query_vector) * np.linalg.norm(v))
            for v in self.vectors
        ]
        ranked = sorted(zip(self.chunks, sims), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


# ---------- 4. Retrieval + generation ----------
def answer_with_rag(question: str, store: SimpleVectorStore):
    query_vector = embed_text(question)
    top_chunks = store.search(query_vector, top_k=3)

    context = "\n\n".join(chunk for chunk, score in top_chunks)

    prompt = (
        f"Use only the context below to answer the question. "
        f"If the answer isn't in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )

    response = bedrock.converse(
        modelId=GEN_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 400, "temperature": 0.2},
    )
    return response["output"]["message"]["content"][0]["text"], top_chunks


if __name__ == "__main__":
    doc = (
        "Amazon Bedrock Guardrails let you configure content filters for both "
        "the input a model receives and the output it produces. Guardrails can "
        "block denied topics, filter PII, and enforce word filters."
    )

    store = SimpleVectorStore()
    for chunk in chunk_text(doc, chunk_size=120, overlap=20):
        store.add(chunk, embed_text(chunk))

    answer, sources = answer_with_rag("What can Bedrock Guardrails filter?", store)
    print("ANSWER:\n", answer)
    print("\nRETRIEVED CHUNKS (with similarity score):")
    for chunk, score in sources:
        print(f"  [{score:.3f}] {chunk}")
