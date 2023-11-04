import http.server

# Set the port you want to use for serving the webpage
port = 8000

# Create a simple HTTP server to serve your webpage
handler = http.server.SimpleHTTPRequestHandler

# Start the server on the specified port
with http.server.HTTPServer(("", port), handler) as httpd:
    print(f"Serving your webpage at http://localhost:{port}")
    httpd.serve_forever()
