from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from flask.cli import load_dotenv
from pymongo import MongoClient
import uuid
from pytz import timezone
import datetime
import os
from werkzeug.utils import secure_filename
UPLOAD_DIR = "D:/"

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR

@app.route('/')
def upload_main():
    return render_template('play.html')