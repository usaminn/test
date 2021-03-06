﻿#-*- coding:utf-8 -*-

# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import re
import glob

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# メッセージをランダムに表示するメソッド
def picked_up():
    messages = [
        "こんにちは、あなたの名前を入力してください",
        "やあ！お名前は何ですか？",
        "あなたの名前を教えてね"
    ]
    # NumPy の random.choice で配列からランダムに取り出し
    return np.random.choice(messages)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "ようこそ"
    message = picked_up()
    # index.html をレンダリングする
    return render_template('index.html',
                           message=message, title=title)

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        name = request.form['name']
        # index.html をレンダリングする
        return render_template('index.html',
                               name=name, title=title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

@app.route('/articles')
def articles():
    title = "ようこそ"
#     article = {}
#    image   = {}
    article = []
    
    adds = glob.glob("static/articles/*")

    for g in adds:
        with open(g,"r",encoding="utf-8") as f:
            while True:
                line = f.readline()
                if line == "":
                    break
                if re.sub(" *img *= *", "img=", line)[:4] == "img=":
                    article.append("img=static/image/"+re.sub(" *img *= *", "img=", line)[4:])
                else:
                    article.append(line)
        article.append("----------------------------------------------------------")
    # index.html をレンダリングする
    return render_template('news.html',
                           article=article, title=title)

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host="ec2-54-250-246-173.ap-northeast-1.compute.amazonaws.com", port=5000) # どこからでもアクセス可能に
#from subprocess import check_output
#from flask import Flask, redirect, request, render_template
#from utils.decorator_auth import requires_auth

#app = Flask(__name__)

@app.before_request
# @requires_auth
def basic_auth():
    pass

#def picked_up():
#    return 0

#@app.route("/")
#def index():
#    return render_template("sample.html")

#if __name__ == "__main__":
#    app.run( debug = True, host="ec2-54-250-246-173.ap-northeast-1.compute.amazonaws.com", port=5000)
