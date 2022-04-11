import sys
import os

from flask import Flask, session, render_template, redirect, request, url_for
import pandas as pd
import json
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

sys.path.append("..") # Adds higher directory to python modules path.
from models.user import User

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'hello'
# 전체 구조 참고 : https://www.section.io/engineering-education/flask-database-integration-with-sqlalchemy/#creating-a-model-in-flask

PORT=5000

load_dotenv(verbose=True) # 환경 변수 세팅(.env)
app = Flask(__name__)

# db
db_uri = f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
# 추가 세팅
# 참고 : https://programmers-sosin.tistory.com/entry/Flask-Flask%EC%97%90%EC%84%9C-SQLAlchemy-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0-Flask-ORM
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 스키마 가져오기 + router 에서 사용하기 위해
import models

db.drop_all()
db.create_all()
db.session.commit() # 실제 적용 시점

#app. py
#현재있는 파일의 디렉토리 절대경로
base_dir = os.path.abspath(os.path.dirname(__file__))

# basdir 경로안에 DB 파일 만들기
db_file = os.path.join(base_dir, 'db. sqlite')

#SQLAlchen 설정

#내가 사용 할 DB URI
app.config['SQLALCHENY DATABASE URI'] = 'sqlite:///' + db_file

#비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_ COMMIT ON TEARDOWN'] = True

#수정사항에 대한 TRACK
app.config[" SOLALCHEMY_TRACK_MODIFICATIONS"] = False

# SECRET KEY
secret_file = os.path.join(base_dir, 'secrets.json') #secrets.json 파일 위치를 명시
with open(secret_file) as f:
  secrets = json. loads(f.read())['SECRET KEY']
app.config['SECRET KEY'] = secrets

db.init_app(app)
db.app = app
db.create_all()

# cors 설정
CORS(app)

# router
from router import create_endpoints
create_endpoints(app)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
