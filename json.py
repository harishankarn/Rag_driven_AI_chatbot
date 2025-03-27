import json

# Function to extract URLs from a JSON file
def get_urls_from_json(json_file_path):
    urls = []
    with open(json_file_path, encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        for item in data:
            urls.append(item['URL'])  # Assumes the JSON contains a list of objects with a 'URL' key
    return urls
