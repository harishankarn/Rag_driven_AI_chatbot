import os
from langchain_community.vectorstores import FAISS


def load_faiss_vector_store(file_path, embeddings):
    """Loads an existing FAISS vector store if available."""
    if os.path.exists(file_path):
        print("Loading existing FAISS index...")
        return FAISS.load_local(file_path, embeddings, allow_dangerous_deserialization=True)
    return None


def create_faiss_vector_store(docs, embeddings):
    """Creates a new FAISS vector store from documents."""
    print("Creating a new FAISS index...")
    return FAISS.from_documents(docs, embeddings)

def save_faiss_vector_store(vector_store, file_path):
    """Saves the FAISS vector store to a file."""
    vector_store.save_local(file_path)


def update_or_create_faiss_vector_store(docs, embeddings, file_path):
    """Updates an existing FAISS index or creates a new one if not found."""
    vector_store = load_faiss_vector_store(file_path, embeddings)
    
    if vector_store:
        vector_store.add_documents(docs)
    else:
        vector_store = create_faiss_vector_store(docs, embeddings)
    
    save_faiss_vector_store(vector_store, file_path)
    return vector_store
