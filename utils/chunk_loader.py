#from langchain_community.document_loaders import WebBaseLoader
#from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_data(urls, chunk_size=1000, chunk_overlap=200): 
    # Load Data from URLs
    #loaders = WebBaseLoader(urls=urls)
    loaders = UnstructuredURLLoader(urls=urls)
    data = loaders.load()
    # data # Print Data

    # faster but less accurate
    # text_splitter = CharacterTextSplitter(separator='\n', chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # slower but more accurate
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""], 
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    
    # Split the loaded documents into smaller chunks
    docs = text_splitter.split_documents(data)
    return docs