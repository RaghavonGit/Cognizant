# Web frameworks receive requests, process them, talk to databases
# and send responses back.
# Django organises code into 3 layers
# Browser Request
#       ↓
#    Middleware      ← "Do you have permission to access this URL?"
#       ↓
#    URLs.py        ← "Which code handles this URL?"
#       ↓
#    View           ← "What should happen?" (your logic lives here)
#       ↓
#    Model          ← "Talk to the database"
#       ↓
#    Response back to browser

# Middleware acts exactly like an airport security checkpoint for your HTTP requests before they reach the router or your view code
# Two types of middleware,
# Security middle ware: protects your site from malicious requests
# Session middleware: manages user sessions, allowing you to store and retrieve data across requests

# Two ways of Django communicating with the web server:
# WSGI (Web Server Gateway Interface) - synchronous, used for traditional web applications, this is default for Django
# ASGI (Asynchronous Server Gateway Interface) - asynchronous, used for real-time applications like chat

# MVC (Model-View-Controller) 
# Model manages the data and logical rules 
# View is the user interface that displays the data to the end user
# Controller is the brains of the operation, accepts user inputs, processes them, and returns the appropriate output to the user

# Layer	File	Responsibility
# Model	models.py	Defines database tables as Python classes
# View	views.py	Handles the request, returns a response
# Template templates/	HTML for browser rendering (we won't use this much — we're building an API)

# MVC Controller  →  Django View    (handles logic, NOT the UI)
# MVC View        →  Django Template (the actual UI/HTML)
# MVC Model       →  Django Model   (same in both)
