#from utils.csv_utils import get_urls_from_csv
from utils.json_utils import get_urls_from_json
from utils.chunk_updater import check_and_update_chunks
from utils.faiss_store import update_or_create_faiss_vector_store
from utils.models import embeddings

#csv_file_path = 'Data/sitemap_data.csv'  # Path to your CSV file
json_file_path = 'Data/sitemap_data.json'  # Path to your JSON file

#urls = get_urls_from_csv(csv_file_path)
urls = get_urls_from_json(json_file_path)
# Use the function to load and split the data
docs = check_and_update_chunks(urls, chunk_size=2000, chunk_overlap=400, chunk_file_path="Data/chunks.pkl")

# Use the function to create and save the FAISS vector store
update_or_create_faiss_vector_store(docs, embeddings, "Data/faiss_store_huggingFace.pkl")