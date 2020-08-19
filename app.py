from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from flask.cli import load_dotenv
from pymongo import MongoClient
from pytz import timezone
app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/info', methods=['POST'])
def resume_info():

    writer_recieve = request.form['writer_give']
    print(writer_recieve)
    document = {
        'writer': writer_recieve,
            }
    db.resume.insert_one(document)

    return jsonify({'result': 'success', 'msg': 'DB등록이 완료 되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

