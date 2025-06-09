from flask import Flask
from config import *
from manual_utils import build_or_load_index
from routes import register_routes

app = Flask(__name__)
app.secret_key = SECRET_KEY

index, chunks = build_or_load_index()
app.index = index
app.chunks = chunks

register_routes(app)
