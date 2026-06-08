import requests
from bs4 import BeautifulSoup
import re
import time
import json
from urllib.parse import urlparse

# ----------------------------
# CONFIG
# ----------------------------
URLS = [
    "https://www.yelp.com/biz/centerpointe-dining-commons-pomona",
    "https://www.opentable.com/landmark/restaurants-near-california-state-polytechnic-university-pomona",
    "https://cppdining.com/eat-well-cpp/",
    "https://www.cpp.edu/aboutcpp/visitor-information/dining.shtml",
    "https://thepolypost.com/arts-and-culture/2020/02/04/review-centerpointe-dining-commons-is-the-new-go-to-spot/",
    "https://www.reddit.com/r/CalPolyPomona/comments/1fg56da/cpp_dining_tier_list/",
    "https://www.reddit.com/r/CalPolyPomona/search/?q=dining",
    "https://www.tripadvisor.com/RestaurantsNear-g32911-d5789363-California_State_Polytechnic_University_Pomona-Pomona_California.html",
    "https://www.niche.com/colleges/california-state-polytechnic-university-pomona/reviews/",
    "https://www.cpp.edu/housing/dining.shtml"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

TIMEOUT = 25
CHUNK_SIZE = 400
OVERLAP = 80


# ----------------------------
# CLEANING
# ----------------------------
def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9.,!?'/\-() ]+", " ", text)
    return text.strip()


def is_bad_page(text: str) -> bool:
    bad_signals = [
        "enable javascript",
        "disable any ad blocker",
        "please enable js",
        "blocked",
        "access denied",
        "just a moment",
        "captcha",
        "robot",
        "sign in to continue"
    ]
    t = text.lower()
    return any(sig in t for sig in bad_signals) or len(t.strip()) < 50


# ----------------------------
# EXTRACTION
# ----------------------------
def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return clean_text(text)


# ----------------------------
# CHUNKING
# ----------------------------
def chunk_text(text: str, chunk_size=400, overlap=80):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunk_str = " ".join(chunk).strip()

        if len(chunk_str) > 80:
            chunks.append(chunk_str)

        i += chunk_size - overlap

    return chunks


# ----------------------------
# FETCH
# ----------------------------
def fetch_url(url: str):
    try:
        print(f"\nProcessing: {url}")

        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        html = resp.text

        text = extract_text(html)

        print("\n--- CLEANED TEXT SAMPLE ---")
        print(text[:300])

        if is_bad_page(text):
            print(f"Skipped (bad page): {url}")
            return []

        chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)

        print(f"Added {len(chunks)} chunks")
        return chunks  # IMPORTANT: return raw chunks only

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        return []


# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    all_chunks = []
    global_chunk_id = 0  # FIX: unique IDs across ALL sources

    for url in URLS:
        chunks = fetch_url(url)

        for chunk in chunks:
            all_chunks.append({
                "source": url,
                "chunk_id": global_chunk_id,
                "text": chunk
            })
            global_chunk_id += 1

        time.sleep(1)

    print("\n========================")
    print(f"TOTAL CHUNKS: {len(all_chunks)}")
    print("========================\n")

    print("SAMPLE CHUNKS (FIRST 5):\n")

    for i, c in enumerate(all_chunks[:5]):
        print(f"--- Chunk {i} ---")
        print("Source:", c["source"])
        print("Word count:", len(c["text"].split()))
        print(c["text"][:500])
        print()

    print("\nRANDOM CHUNK INSPECTION:\n")

    import random
    for _ in range(min(3, len(all_chunks))):
        c = random.choice(all_chunks)
        print("--- RANDOM CHUNK ---")
        print("Source:", c["source"])
        print("Word count:", len(c["text"].split()))
        print(c["text"][:500])
        print()

    # ----------------------------
    # REQUIRED FOR MILESTONE 4
    # ----------------------------
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print("\nSaved → chunks.json")


if __name__ == "__main__":
    main()