from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter

def load_and_split_data(urls, chunk_size=1000, chunk_overlap=200):
    # Load Data from URLs
    loaders = UnstructuredURLLoader(urls=urls)
    data = loaders.load()
    # data # Print Data

    # Initialize the text splitter with specified parameters
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    # Split the loaded documents into smaller chunks
    docs = text_splitter.split_documents(data)
    return docs