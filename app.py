from flask import Flask
app = Flask(__name__) 

@app.route("/")
def home():
    return "Whatever it takes"

@app.route("/stores")
def store():
    return "Number of Stores"

from controller import *
