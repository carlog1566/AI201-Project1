import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb

# ----------------------------
# LOAD MODELS
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

model = SentenceTransformer("all-MiniLM-L6-v2")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_collection("cpp_dining")


# ----------------------------
# RETRIEVAL
# ----------------------------
def retrieve(query, k=4):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    chunks = results["documents"][0]
    metas = results["metadatas"][0]

    context = []
    sources = []

    for i in range(len(chunks)):
        context.append(f"[Source: {metas[i]['source']}]\n{chunks[i]}")
        sources.append(metas[i]["source"])

    return "\n\n".join(context), list(set(sources))


# ----------------------------
# GENERATION (THIS REPLACES "ask")
# ----------------------------
def ask(query):
    context, sources = retrieve(query)

    prompt = f"""
You are answering questions about Cal Poly Pomona dining.

RULES:
- Use ONLY the provided context.
- If context is insufficient, say "I don't have enough information from the sources."
- Do NOT use outside knowledge.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }