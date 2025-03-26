from langchain_huggingface import HuggingFaceEmbeddings

# Centralized Embeddings
#EMBEDDING_MODEL_NAME = " intfloat/e5-base-v2"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# Centralized LLM Repo ID
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
