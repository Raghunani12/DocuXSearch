from flask import Flask, render_template, request, jsonify
import os
from urllib.parse import urlparse, unquote
from scrapers.google_scraper import search_google

app = Flask(__name__)

# Function to check if a URL ends with a document extension
def is_document_url(url):
    document_extensions = ['.pdf', '.docx', '.pptx', '.xls', '.xlsx']  # Add more extensions as needed
    parsed_url = urlparse(url)
    path = parsed_url.path
    for ext in document_extensions:
        if path.endswith(ext):
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    concept = request.form['concept']
    num_results = int(request.form['num_results'])
    print(f"Searching for: {concept} with {num_results} results")
    search_results = search_google(concept, num_results)
    
    print(f"Search results: {search_results}")

    documents = []
    for result in search_results:
        file_name = os.path.basename(result)
        if concept.lower() in file_name.lower() and is_document_url(result):
            documents.append({
                'url': result,
                'file_name': file_name
            })
    
    print(f"Filtered documents: {documents}")
    
    return jsonify(documents)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
