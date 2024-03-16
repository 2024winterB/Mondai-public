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

# タイムゾーンを設定
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# cronをインストール
RUN apt-get install -y cron
# cronファイルをコピー
COPY ./Mondai/cron /etc/cron.d/cron
# cronファイルの権限を設定
RUN chmod 0644 /etc/cron.d/cron
# .shファイルをコピー
COPY ./Mondai/date.sh /code/date.sh
COPY ./Mondai/mail.sh /code/mail.sh
# .shファイルの権限を設定
RUN chmod +x /code/mail.sh /code/date.sh
# cronを登録
RUN crontab /etc/cron.d/cron
