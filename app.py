from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from flask.cli import load_dotenv
from pymongo import MongoClient
import uuid
from pytz import timezone
import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.

UPLOAD_DIR = "BASE_FOLDER"
app.config['UPLOAD_DIR'] = UPLOAD_DIR




app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbsparta
# app.config['UPLOAD_DIR'] = UPLOAD_DIR


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list')
def list():
    return render_template('showDB.html')


@app.route('/info', methods=['POST'])
def resume_info():
    # DB입력 정보 가져오기
    writer_recieve = request.form['writer_give']
    name_recieve = request.form['name_give']
    birth_recieve = request.form['birth_give']
    email_recieve = request.form['email_give']
    phone_recieve = request.form['phone_give']
    salary_recieve = request.form['salary_give']
    univ_recieve = request.form['univ_give']
    career_recieve = request.form['career_give']
    company_recieve = request.form['company_give']
    file_uuid = str(uuid.uuid4)
    print(writer_recieve)

    document = {
        'writer': writer_recieve, 'name': name_recieve, 'birth': birth_recieve, 'email': email_recieve,
        'phone': phone_recieve, 'salary': salary_recieve, 'univ': univ_recieve, 'career': career_recieve,
        'company': company_recieve
    }
    print(document)

    db.resume.update_one(document, {'$set': {'uuid': file_uuid, **document}}, upsert=True)

    return jsonify({'result': 'success', 'msg': 'DB등록이 완료 되었습니다.'})


# @app.route('/readinfo', methods=['POST'])
# def read_info():
#     # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
#     data = list(db.resume.find({}, {'_id': 0}))
#     # 2. articles라는 키 값으로 articles 정보 보내주기
#     result = {
#         'result': 'success',
#         'data': data,
#     }



@app.route('/file-upload', methods=['GET', 'POST'])
def upload_files():
    # if request.method == 'POST':
    #     f = request.files['file']
    #     # fname = secure_filename(f.filename)
    #     # path = os.path.join(app.config['UPLOAD_DIR'], fname)
    #     f.save('BASE_FOLDER'+secure_filename(f.filename))
    #     return '성공'
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_DIR'], fname)
        f.save(path)
        return 'File upload complete (%s)' % path

# author_recieve = request.form['author_give']
# print(author_recieve)
# document = {
#     'author': author_recieve,
#         }


# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     document = {
#         'resume' :
#     }
#     return '성공'
#
#     # return send_from_directory(directory='file', filename=filename)
# @app.route('/upload', methods=['POST'])
# def upload():



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
