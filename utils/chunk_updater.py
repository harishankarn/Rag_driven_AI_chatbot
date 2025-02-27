import os
import pickle
from utils.chunk_loader import load_and_split_data

# Define a function to check for new changes and update the chunks
def check_and_update_chunks(urls, chunk_size=1000, chunk_overlap=200, chunk_file_path="Data/chunks.pkl"):
    if os.path.exists(chunk_file_path):
        with open(chunk_file_path, "rb") as f:
            docs = pickle.load(f)
    else:
        docs = load_and_split_data(urls, chunk_size, chunk_overlap)
        with open(chunk_file_path, "wb") as f:
            pickle.dump(docs, f)
    return docs