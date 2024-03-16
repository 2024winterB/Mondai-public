# Pythonのイメージを指定
FROM python:3.10.7-buster

# PYTHONDONTWRITEBYTECODEとPYTHONUNBUFFEREDはオプション
# pycファイル(および__pycache__)の生成を行わないようにする
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED=1
# コンテナにcodeワークディレクトリを作成
RUN mkdir /code
# コンテナのワークディレクトリを/codeに指定
WORKDIR /code

# ローカルのDocker/Django/requirements.txtをコンテナの/codeフォルダ直下に置く
COPY ./Docker/Django/requirements.txt /code/
# コンテナ内でpip install -r requirements.txtを実行
RUN apt update -y && \
    pip install -U pip && \
    pip install -r requirements.txt && \
    # mecabをインストール
    apt-get update && apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8
# ソースコードをコンテナにコピー
COPY . /code/
