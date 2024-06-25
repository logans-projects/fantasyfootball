from flask import Flask
import dash
import os

from app import create_dash_app  # Adjust this import based on your app.py

server = Flask(__name__)
app = create_dash_app(server)

# This is required for Vercel to serve the app
def handler(event, context):
    from mangum import Mangum
    asgi_handler = Mangum(app.server)
    return asgi_handler(event, context)
