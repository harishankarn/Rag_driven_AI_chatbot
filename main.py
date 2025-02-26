import sys
import os
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Add the utils directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.csv_utils import get_urls_from_csv
from utils.chunk_updater import check_and_update_chunks
from utils.faiss_store import (
    create_and_save_faiss_vector_store,
    load_faiss_vector_store,
)

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.chains import RetrievalQAWithSourcesChain
'''
# Define a function to ask a question using the Retrieval QA chain
def ask_question(question):
    response = chain.invoke({"question": question})  # Use 'question' as key
    answer = response.get("answer", "").strip()  # Ensure 'answer' is the correct key
    return f"Answer: {answer}\n"'''
from transformers import AutoTokenizer

# Load tokenizer for Mistral-7B
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

def ask_question(question):
    # Truncate the question to a reasonable size (max 200 tokens)
    tokenized_question = tokenizer.encode(question, truncation=True, max_length=200)
    truncated_question = tokenizer.decode(tokenized_question)

    # Invoke the retrieval chain
    response = chain.invoke({"question": truncated_question})  

    # Ensure retrieved context is within limits
    if "context" in response:
        tokenized_context = tokenizer.encode(response["context"], truncation=True, max_length=800)
        truncated_context = tokenizer.decode(tokenized_context)
        response["context"] = truncated_context  # Update context in response

    # Get the final answer
    answer = response.get("answer", "").strip()  

    return f"Answer: {answer}\n"

csv_file_path = 'sitemap_data.csv'  # Path to your CSV file
urls = get_urls_from_csv(csv_file_path)

# Use the function to load and split the data
docs = check_and_update_chunks(urls, chunk_size=2000, chunk_overlap=400, chunk_file_path="chunks.pkl")

# Initialize the Hugging Face BGE embeddings
embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
 
# Use the function to create and save the FAISS vector store
create_and_save_faiss_vector_store(docs, embeddings, "faiss_store_huggingFace.pkl")
VectorStore = load_faiss_vector_store("faiss_store_huggingFace.pkl")

Token = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = Token

# Initialize Language Model
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0.7,
    model_kwargs={
        "max_tokens": 150,
        "Token": Token
    }
)

chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=VectorStore.as_retriever())

while True:
    try:
        # Ask a question using the Retrieval QA chain
        question = input("Ask a question: ")
        response = ask_question(question)
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")

