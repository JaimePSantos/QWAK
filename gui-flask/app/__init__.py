import os
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session

QWAKCLUSTER_USERNAME = os.environ.get('QWAKCLUSTER_USERNAME')
QWAKCLUSTER_PASSWORD = os.environ.get('QWAKCLUSTER_PASSWORD')

connection_string = f"mongodb+srv://{QWAKCLUSTER_USERNAME}:{QWAKCLUSTER_PASSWORD}@qwakcluster.kkszzg0.mongodb.net/test"

# client = MongoClient('localhost', 27017)
client = MongoClient(connection_string)
db_string = 'qwak_flask'
database = client.get_database(db_string)
probDistEntry = database['probDistEntry']

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

from app import routes