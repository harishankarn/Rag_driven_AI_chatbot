import sys
import os
import warnings
from dotenv import load_dotenv

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Add the utils directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.faiss_store import load_faiss_vector_store
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQAWithSourcesChain

# Define a function to ask a question using the Retrieval QA chain
def ask_question(chain, question):
    response = chain.invoke({"question": question})  # Use 'question' as key
    answer = response.get("answer", "").strip()  # Ensure 'answer' is the correct key
    return f"Answer: {answer}\n"

def main():
    # Use the function to load the FAISS vector store
    VectorStore = load_faiss_vector_store("Data/faiss_store_huggingFace.pkl")

    # Initialize Language Mode
    load_dotenv()
    
    Token = os.getenv('HuggingFaceToken')
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = Token

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
            response = ask_question(chain, question)
            print(response)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()