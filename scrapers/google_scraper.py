import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

def search_google(query, num_results=10):
    search_url = f"https://www.google.com/search?q={query}+filetype:pdf+OR+filetype:docx+OR+filetype:pptx&num={num_results}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/url?q=' in href:
            link = parse_qs(urlparse(href).query).get('q', [None])[0]
            if link:
                links.append(unquote(link))
    return links

# Example Usage
if __name__ == '__main__':
    search_results = search_google('machine learning concepts')
    for result in search_results:
        print(result)
