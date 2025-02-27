import sys
import os
import warnings
from dotenv import load_dotenv
from utils.faiss_store import load_faiss_vector_store
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEndpoint

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Add the utils directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Use the function to load the FAISS vector store
VectorStore = load_faiss_vector_store("Data/faiss_store_huggingFace.pkl")
retriever=VectorStore.as_retriever()

# Load the Hugging Face API token from the .env file
load_dotenv()
Token = os.getenv('HuggingFaceToken')
os.environ["HUGGINGFACEHUB_API_TOKEN"] = Token

# Define the Hugging Face repository ID
repo_id="mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    temperature=0.7,
    model_kwargs={
        "max_tokens": 150,
        "Token": Token
    }
)

# Initialize memory to maintain conversation context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the conversational retrieval chain
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

def ask_question(chain, question):
    response = chain.invoke({"question": question})
    answer = response.get("answer", "").strip()
    return f"Answer: {answer}\n"


if __name__ == "__main__":
    while True:
        try:
            # Ask a question using the Retrieval QA chain
            question = input("Ask a question: ")
            response = ask_question(chain, question)
            print(response)
        except Exception as e:
            print(f"An error occurred: {e}")
