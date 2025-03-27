import csv

# Function to extract URLs from a CSV file
def get_urls_from_csv(csv_file_path):
    urls = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urls.append(row['URL'])  # Assumes the CSV has a column named 'URL'
    return urls