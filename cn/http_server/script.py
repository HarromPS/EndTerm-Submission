'''
USAGE:

python script.py

open in browser by typing = localhost:5555
'''

# importing all the functions
# from http.server module
from http.server import *

# creating a class for handling
# basic Get and Post Requests
class HandlerFunction(BaseHTTPRequestHandler):

	# creating a function for Get Request
	def do_GET(self):

		# Success Response --> 200
		self.send_response(200)

		# Type of file that we are using for creating our
		# web server.
		self.send_header('content-type', 'text/html')
		self.end_headers()

		# what we write in this function it gets visible on our
		# web-server
		self.wfile.write('<h1>Hello Guys<br/>This is a Http Server</h1>'.encode())


# this is the object which take port
# number and the server-name
# for running the server
# Use try-except block to handle KeyboardInterrupt
try:
    # Start the HTTP server on port 5555
    with HTTPServer(('localhost', 5555), HandlerFunction) as server:
        print('Server started on http://localhost:5555')
        # this is used for running our
        # server as long as we wish
        # i.e. forever
        server.serve_forever()
except KeyboardInterrupt:
    print('\nServer stopped')


'''
To run the application we need two servers
1. to run the server: python -m htt.server
2. to make a request: python filename.py
'''