import os
import pickle
import hashlib
from utils.chunk_loader import load_and_split_data

def hash_urls(urls):
    """Creates a hash of URLs to check if they have changed."""
    return hashlib.md5("".join(sorted(urls)).encode()).hexdigest()

def check_and_update_chunks(urls, chunk_size=1000, chunk_overlap=200, chunk_file_path="Data/chunks.pkl", hash_file_path="Data/urls_hash.txt"):
    """Checks if new URLs are present and updates chunks accordingly."""
    
    # Compute hash of current URLs
    current_hash = hash_urls(urls)

    # Check if existing hash file is available
    if os.path.exists(hash_file_path):
        with open(hash_file_path, "r") as f:
            saved_hash = f.read().strip()
    else:
        saved_hash = None

    # Load existing chunks if hash matches
    if saved_hash == current_hash and os.path.exists(chunk_file_path):
        with open(chunk_file_path, "rb") as f:
            docs = pickle.load(f)
    else:
        print("Detected new URLs or changes, updating chunks...")
        docs = load_and_split_data(urls, chunk_size, chunk_overlap)
        with open(chunk_file_path, "wb") as f:
            pickle.dump(docs, f)
        
        # Save new hash
        with open(hash_file_path, "w") as f:
            f.write(current_hash)

    return docs
