
with ease.Click on function and method calls to jump to their definitions or references in the same repository.Learn more

import datetime
import os
import uuid
from urllib.parse import urlparse

import slack
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)
from flask.cli import load_dotenv
from pymongo import MongoClient
from pytz import timezone

app = Flask(__name__)
load_dotenv()

LEO_HOST = os.environ['LEO_HOST']
FLASK_ENV = os.environ['FLASK_ENV']
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
UPLOAD_PASSWORD = os.environ['UPLOAD_PASSWORD']
ALLOWED_EXTENSIONS = {'html'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PASSWORD'] = UPLOAD_PASSWORD

if FLASK_ENV == 'test':
    mongo_client = MongoClient(os.environ['MONGO_TEST_CLIENT_URI'], 27017)
    db_name = os.environ['MONGO_TEST_DB_NAME']
else:
    mongo_client = MongoClient(os.environ['MONGO_CLIENT_URI'], 27017)
    db_name = os.environ['MONGO_DB_NAME']
db = getattr(mongo_client, db_name)

slack_client = None if FLASK_ENV == 'test' else slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
SLACK_CLASS_CHANNEL = os.environ.get('SLACK_CLASS_CHANNEL', '')
SLACK_TUTOR_MEMBER_ID = os.environ.get('SLACK_TUTOR_MEMBER_ID', '')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/homework/<string:author>/<string:title>', methods=['POST'])
def upload_homework(author, title):
    upload_time = datetime.datetime.now(timezone('Asia/Seoul'))
    homework_name = {'title': title, 'author': author}

    if file := request.files.get('file'):
        homework = db.homework.find_one(homework_name)

        if file_uuid := homework.get('uuid'):
            filename = f'{file_uuid}.html'
        else:
            new_file_uuid = uuid.uuid4()
            filename = f'{new_file_uuid}.html'

        filepath = os.path.join(BASE_FOLDER, app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        db.homework.update(homework_name, {'$set': {'filepath': filepath, 'upload_time': upload_time}})

        if slack_client:
            slack_msg = f':trophy::trophy::trophy: {author} 님의 {title} 웹페이지를 업로드했습니다.'
            if SLACK_TUTOR_MEMBER_ID:
                slack_msg += f' <@{SLACK_TUTOR_MEMBER_ID}>'
            homework_url = urlparse(f'http://{LEO_HOST}/homework/{author}/{title}').geturl()
            slack_msg += f'\n<{homework_url}|과제 페이지로 이동>'
            try:
                slack_client.chat_postMessage(channel=SLACK_CLASS_CHANNEL, text=slack_msg)
            except Exception:
                pass

        result = {'result': 'success', 'msg': '숙제가 성공적으로 등록되었습니다.'}

    else:
        result = {'result': 'fail', 'msg': '숙제 파일이 없습니다.'}

    return jsonify(result)


@app.route('/homework', methods=['POST'])
def submit_homework():
    title_receive = request.form['title_give']
    author_receive = request.form['author_give']
    password_receive = request.form['password_give']
    file_uuid = str(uuid.uuid4())

    if password_receive != app.config['UPLOAD_PASSWORD']:
        return jsonify({'result': 'fail', 'msg': '비밀번호가 틀렸습니다.'})

    homework_name = {'title': title_receive, 'author': author_receive}

    db.homework.update_one(homework_name, {'$set': {'uuid': file_uuid, **homework_name}}, upsert=True)
    return jsonify({'result': 'success', 'msg': '숙제가 성공적으로 등록되었습니다.'})


@app.route('/homework', methods=['GET'])
def read_homework():
    homework = list(db.homework.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'homework': homework})


@app.route('/homework/<string:author>/<string:title>', methods=['GET'])
def get_homework(author, title):
    homework_name = {'title': title, 'author': author}
    homework = db.homework.find_one(homework_name)
    filename = os.path.split(homework.get('filepath'))[-1]
    return send_from_directory(os.path.join(BASE_FOLDER, app.config['UPLOAD_FOLDER']), filename)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
