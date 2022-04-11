import sys

from flask import jsonify
import pandas as pd
import json


sys.path.append("..") # Adds higher directory to python modules path.
from models.user import User

def create_endpoints(app):
  @app.route('/')
  def hello_world():
    return 'Hello World!'

  @app.route('/users')
  def get_all_users():
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    queryset = User.query.all()

    # # 안됨
    # print(queryset.statement)
    # print(queryset.session.bind)
    # # https://blog.naver.com/PostView.nhn?blogId=varkiry05&logNo=221485216965&categoryNo=107&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=search
    # df = pd.read_sql(queryset.statement, queryset.session.bind)

    # result = json.loads(df.to_json())
    # print(result)

    result = queryset[0]

    if result is None:
      return ''
    return jsonify(result.name)
