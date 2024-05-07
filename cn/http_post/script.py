'''
USAGE:

python script.py

open in browser by typing = localhost:5555
'''


from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests

class HandlerFunction(BaseHTTPRequestHandler):
    # creating a function for Get Request
    def do_GET(self):
        # Success Response --> 200
        self.send_response(200)

        # Type of file that we are using for creating our
        # web server.
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # HTML form to get user input
        html = """
        <html>
        <head><title>Input Form</title></head>
        <body>
            <h1>Enter URL to Fetch a Response:</h1>
            <form method="POST">
                <input type="text" name="url" value="https://www.google.com">
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """

        # what we write in this function it gets visible on our
        # web-server

        self.wfile.write(html.encode())

    # creating a function for Post Request
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Parse the POST data to get the value of 'url'
        parsed_data = urllib.parse.parse_qs(post_data)
        url = parsed_data.get('url', [''])[0]

        # Process the input and generate output
        # For demonstration, let's just echo back the input URL
        # response = f"<html><body><h1>Entered URL: {url}</h1></body></html>"

        # make a request to the url server and returns its html response
        try:
            res = requests.get(url)
            html_response = res.text
            response = f"{html_response}"
        except Exception as e:
            # Handle exceptions if the request fails
            html_response = f"Error fetching URL: {e}"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(response.encode())

# Run the server
def run(server_class=HTTPServer, handler_class=HandlerFunction, port=5555):
    try:
        # Start the HTTP server on port 5555
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print(f"Server started on http://localhost:{port}")

        # this is used for running our
        # server as long as we wish
        # i.e. forever
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped')

if __name__ == "__main__":
    run()
