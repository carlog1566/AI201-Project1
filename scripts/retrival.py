import json
from sentence_transformers import SentenceTransformer
import chromadb

# ----------------------------
# LOAD CHUNKS
# ----------------------------
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]
metadatas = [
    {
        "source": c["source"],
        "chunk_id": c["chunk_id"]
    }
    for c in chunks
]

ids = [str(i) for i in range(len(chunks))]

# ----------------------------
# EMBEDDING MODEL
# ----------------------------
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Creating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

# ----------------------------
# CHROMA DB SETUP
# ----------------------------
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="cpp_dining")

# ----------------------------
# STORE DATA
# ----------------------------
print("Storing in ChromaDB...")

collection.add(
    embeddings=embeddings.tolist(),
    documents=texts,
    metadatas=metadatas,
    ids=ids
)

print("DONE: Vector DB built successfully")

# ----------------------------
# RETRIEVAL FUNCTION
# ----------------------------
def search(query, k=4):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    print("\n==============================")
    print(f"QUERY: {query}")
    print("==============================\n")

    for i in range(k):
        print(f"Result {i+1}")
        print("Source:", results["metadatas"][0][i]["source"])
        print("Chunk ID:", results["metadatas"][0][i]["chunk_id"])
        print("Text:", results["documents"][0][i][:300])
        print("-" * 50)

    return results


# ----------------------------
# TEST QUERIES (IMPORTANT FOR MILESTONE 4)
# ----------------------------
if __name__ == "__main__":

    search("What do students think about Centerpointe dining quality?")
    search("Which dining place has the longest wait times at CPP?")
    search("Is CPP dining worth the meal plan?")