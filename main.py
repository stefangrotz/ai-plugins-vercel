from http.server import BaseHTTPRequestHandler
import urllib.parse
import requests
import json

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Parse query parameters
        path, _, query_string = self.path.partition('?')
        params = urllib.parse.parse_qs(query_string)
        title = params.get('title', [''])[0]  # Use the 'title' parameter value if it exists, or '' if it doesn't

        # Fetch data from Wikipedia
        response = requests.get('https://de.wikipedia.org/w/api.php', params={
            'format': 'json',
            'action': 'query',
            'prop': 'extracts',
            'exintro': '1',
            'explaintext': '1',
            'titles': title,
        })
        data = response.json()

        # Extract the page extract text
        pages = data['query']['pages']
        page = next(iter(pages.values()))
        extract = page.get('extract', '')

        # Send the response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'title': title, 'extract': extract}).encode('utf-8'))

        return
