import requests
import xml.etree.ElementTree as ET
import csv
import json
import time
from bs4 import BeautifulSoup

sitemap_urls = [
    "https://www.amrita.edu/post-sitemap.xml",
    "https://www.amrita.edu/page-sitemap1.xml",
    "https://www.amrita.edu/page-sitemap2.xml",
    "https://www.amrita.edu/page-sitemap3.xml",
    "https://www.amrita.edu/page-sitemap4.xml",
    "https://www.amrita.edu/am-event-sitemap1.xml",
    "https://www.amrita.edu/am-event-sitemap2.xml",
    "https://www.amrita.edu/am-event-sitemap3.xml",
    "https://www.amrita.edu/am-event-sitemap4.xml",
    "https://www.amrita.edu/campus-sitemap.xml",
    "https://www.amrita.edu/department-sitemap1.xml",
    "https://www.amrita.edu/school-sitemap1.xml",
    "https://www.amrita.edu/center-sitemap1.xml",
    "https://www.amrita.edu/school-sitemap2.xml",
    "https://www.amrita.edu/program-sitemap1.xml",
    "https://www.amrita.edu/program-sitemap2.xml",
    "https://www.amrita.edu/course-sitemap1.xml",
    "https://www.amrita.edu/course-sitemap2.xml",
    "https://www.amrita.edu/course-sitemap3.xml",
    "https://www.amrita.edu/course-sitemap4.xml",
    "https://www.amrita.edu/course-sitemap5.xml",
]


webpage_urls = []

def fetch_xml(url):
    """Fetch and parse XML sitemap"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return ET.fromstring(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sitemap {url}: {e}")
        return None

def extract_urls_from_sitemap(sitemap_url):
    """Extract URLs from a given sitemap"""
    root = fetch_xml(sitemap_url)
    if root is None:
        return


    namespace = root.tag.split("}")[0].strip("{") if "}" in root.tag else ""
    ns = {"ns": namespace} if namespace else {}

 
    for url in root.findall("ns:url", ns) if namespace else root.findall("url"):
        loc = url.find("ns:loc", ns).text if namespace else url.find("loc").text
        webpage_urls.append(loc)


for sitemap in sitemap_urls:
    extract_urls_from_sitemap(sitemap)

print(f"\nExtracted {len(webpage_urls)} URLs from sitemaps.\n")


def extract_webpage_content(url):
    """Fetch webpage content and extract text"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")

        
        title = soup.title.string if soup.title else url.strip("/").split("/")[-1].replace("-", " ").title()

        
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text() for p in paragraphs])

        return {"url": url, "title": title, "content": content}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage {url}: {e}")
        return {"url": url, "title": "Error", "content": "Failed to retrieve content"}


scraped_data = []
for idx, url in enumerate(webpage_urls[:50000]):  
    print(f"Scraping {idx+1}/{len(webpage_urls)}: {url}")
    data = extract_webpage_content(url)
    scraped_data.append(data)
    time.sleep(1)  

csv_file = "sitemap_data.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "URL", "Content"])
    for row in scraped_data:
        writer.writerow([row["title"], row["url"], row["content"]])

print(f"\nData saved to {csv_file}")

json_file = "sitemap_data.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4)

print(f"Data also saved to {json_file}")
