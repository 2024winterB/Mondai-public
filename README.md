# 2024winterB

問題共有学習アプリ

## 使用技術一覧

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- フロントエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-javascript-ff8c00.svg?logo=javascript&style=for-the-badge">
  <img src="https://img.shields.io/badge/-html5-ffffff.svg?logo=html5&style=for-the-badge">
  <img src="https://img.shields.io/badge/-css3-1572B6.svg?logo=css3&style=for-the-badge">
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <!-- バックエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=for-the-badge">
  <!-- ミドルウェア一覧 -->
  <img src="https://img.shields.io/badge/-Nginx-269539.svg?logo=nginx&style=for-the-badge">
  <img src="https://img.shields.io/badge/-MySQL-4479A1.svg?logo=mysql&style=for-the-badge&logoColor=white">
  <!-- インフラ一覧 -->
  <img src="https://img.shields.io/badge/-Docker-e0ffff.svg?logo=docker&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Amazon%20aws-232F3E.svg?logo=amazon-aws&style=for-the-badge">
</p>

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [開発環境構築](#開発環境構築)
5. [トラブルシューティング](#トラブルシューティング)
   <br />

<!-- プロジェクト名を記載 -->

## プロジェクト名

Linkey
<br><br>

<!-- プロジェクトについて -->

## プロジェクトについて

問題共有学習アプリ

<!-- プロジェクトの概要を記載 -->

- キーワード(用語)ごとに問題を作り、関連するキーワードと紐付ける。
- 過去の成績、前回テストからの経過日数をもとに理解の悪い問題を出題
- 1 つのキーワードに、みんなが問題を作成できる形に。Teachers Takes All をもっと気軽に実現。
- 問題を作る際、chatGPT に解説を書いてもらえるボタンを実装

<p align="right">(<a href="#top">トップへ</a>)</p>

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワークなど | バージョン    |
| ------------------------ | ------------- |
| Python                   | 3.10.7-buster |
| Django                   | <4            |
| uwsgi                    |               |
| MySQL                    | 8.0           |
| mysqlclient              | 2.1.1         |
| docker compose           | 3.9           |
| openai                   | 0.28.1        |
| nginx 1.24.0             | 1.24.0        |
| redis                    | latest        |

| Dockerimage として使用 | バージョン |
| ---------------------- | ---------- |
| MySQL                  | 8.0        |
| nginx 1.24.0           | 1.24.0     |
| redis                  | latest     |

## その他、requirements.txt の内容

```
Django<4
mysqlclient == 2.1.1
scikit-learn == 1.4.0

# Nginx使うならuwsgi必要
uwsgi

#PWA関係
django-pwa

# chatGPT関係
langchain
openai == 0.28.1

#mecab関係
mecab-python3
```

<p align="right">(<a href="#top">トップへ</a>)</p>

## ディレクトリ構成

<!-- Treeコマンドを使ってディレクトリ構成を記載 -->
<pre>
.
└── Mondai
    ├── Docker
    │   ├── Django
    │   │   ├── Dockerfile
    │   │   └── requirements.txt
    │   ├── MySQL
    │   │   ├── Dockerfile
    │   │   └── init.sql
    │   └── Nginx
    │       ├── Dockerfile
    │       ├── conf
    │       │   └── my_nginx.conf
    │       └── uwsgi_params
    ├── Mondai
    │   ├── Mondai_app
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── forms.py
    │   │   ├── migrations
    │   │   │   ├── 0001_initial.py
    │   │   │   ├── 0002_auto_20240225_1033.py
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── static
    │   │   │   ├── css
    │   │   │   ├── icons
    │   │   │   ├── images
    │   │   │   └── js
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── Mondai_project
    │   │   ├── __init__.py
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── manage.py
    │   └── templates
    │       ├── answer.html
    │       ├── base.html
    │       ├── change-password.html
    │       ├── changedone-password.html
    │       ├── create-keyword.html
    │       ├── create-question.html
    │       ├── detail-question.html
    │       ├── edit-user.html
    │       ├── favorite-questions.html
    │       ├── home.html
    │       ├── loading.html
    │       ├── login.html
    │       ├── mine.html
    │       ├── questions.html
    │       ├── regist.html
    │       ├── sidebar.html
    │       ├── sw.js
    │       ├── test.html
    │       ├── update-keyword.html
    │       ├── update-question.html
    │       ├── userprofile.html
    │       ├── 不要list-choice.html
    │       └── 不要others.html
    ├── README.md
    ├── docker-compose.yml
    ├── mysql_data
    ├── phpmyadmin
    ├── pull_request_template.md
    └── static
        ├── admin
        │   ├── css
        │   │   ├── autocomplete.css
        │   │   ├── base.css
        │   │   ├── changelists.css
        │   │   ├── dashboard.css
        │   │   ├── fonts.css
        │   │   ├── forms.css
        │   │   ├── login.css
        │   │   ├── nav_sidebar.css
        │   │   ├── responsive.css
        │   │   ├── responsive_rtl.css
        │   │   ├── rtl.css
        │   │   ├── vendor
        │   │   └── widgets.css
        │   ├── fonts
        │   │   ├── LICENSE.txt
        │   │   ├── README.txt
        │   │   ├── Roboto-Bold-webfont.woff
        │   │   ├── Roboto-Light-webfont.woff
        │   │   └── Roboto-Regular-webfont.woff
        │   ├── img
        │   │   ├── LICENSE
        │   │   ├── README.txt
        │   │   ├── calendar-icons.svg
        │   │   ├── gis
        │   │   ├── icon-addlink.svg
        │   │   ├── icon-alert.svg
        │   │   ├── icon-calendar.svg
        │   │   ├── icon-changelink.svg
        │   │   ├── icon-clock.svg
        │   │   ├── icon-deletelink.svg
        │   │   ├── icon-no.svg
        │   │   ├── icon-unknown-alt.svg
        │   │   ├── icon-unknown.svg
        │   │   ├── icon-viewlink.svg
        │   │   ├── icon-yes.svg
        │   │   ├── inline-delete.svg
        │   │   ├── search.svg
        │   │   ├── selector-icons.svg
        │   │   ├── sorting-icons.svg
        │   │   ├── tooltag-add.svg
        │   │   └── tooltag-arrowright.svg
        │   └── js
        │       ├── SelectBox.js
        │       ├── SelectFilter2.js
        │       ├── actions.js
        │       ├── admin
        │       ├── autocomplete.js
        │       ├── calendar.js
        │       ├── cancel.js
        │       ├── change_form.js
        │       ├── collapse.js
        │       ├── core.js
        │       ├── inlines.js
        │       ├── jquery.init.js
        │       ├── nav_sidebar.js
        │       ├── popup_response.js
        │       ├── prepopulate.js
        │       ├── prepopulate_init.js
        │       ├── urlify.js
        │       └── vendor
        ├── css
        │   ├── answer.css
        │   ├── base.css
        │   ├── basics.css
        │   ├── create-keyword.css
        │   ├── create-question.css
        │   ├── edituser-modal.css
        │   ├── home.css
        │   ├── keyword.css
        │   ├── list.css
        │   ├── loading.css
        │   ├── login.css
        │   ├── modal.css
        │   ├── sidebar.css
        │   ├── test.css
        │   └── userprofile.css
        ├── icons
        │   ├── icon-192x192.png
        │   └── icon-512x512.png
        ├── images
        │   ├── ei_arrow-down.png
        │   ├── ei_arrow-right.png
        │   ├── eye-off.png
        │   ├── eye-on.png
        │   ├── home.png
        │   ├── key.png
        │   ├── link_arrow-right.png
        │   ├── linkey.ico
        │   ├── loading.gif
        │   ├── logout.png
        │   ├── mdi_star-outline.png
        │   ├── mdi_star.png
        │   ├── my_question.png
        │   ├── new_category.png
        │   ├── other_question.png
        │   ├── pencil.png
        │   ├── shmdi_star.png
        │   ├── tabler_search.png
        │   ├── trash.png
        │   ├── user_information.png
        │   └── white_key.png
        └── js
            ├── change-password.js
            ├── change-profile.js
            ├── changed-keywords.js
            ├── created-keywords.js
            ├── link.js
            ├── loading.js
            ├── manifest.json
            ├── modal.js
            ├── sidebar.js
            ├── tag-error.js
            └── text-length.js
</pre>

<p align="right">(<a href="#top">トップへ</a>)</p>

## 開発環境構築

<!-- コンテナの作成方法、パッケージのインストール方法など、開発環境構築に必要な情報を記載 -->

### コンテナの作成と起動

1. Django の初期設定コマンドで環境を構築

2. Nginx,Django,MySQL の Dockerfile を作成　※Nginx は開発中はコメントアウト

3. docker-compose.yml を作成

4. 以上を修正後、以下のコマンドで環境を構築

docker compose up --build

<br><br>

### 動作確認

http://localhost:8000 にアクセスできるか確認　※Nginx 使用時は http://localhost:80
アクセスできたら成功

### コンテナの停止

以下のコマンドでコンテナを停止することができます

docker compose stop

### 環境変数の一覧

| 変数名               | 役割                                                                                   |
| -------------------- | -------------------------------------------------------------------------------------- |
| SECRET_KEY           | Django のシークレットキー（Django の project 新規作成時に settings.py に記載される。） |
| DJANGO_ALLOWED_HOSTS | Django にリクエストを許可するホスト名                                                  |
| DEBUG                | デバッグモードの切り替え                                                               |
| MYSQL_ROOT_PASSWORD  | MySQL のルートパスワード（Docker で使用）                                              |
| MYSQL_DATABASE       | MySQL のデータベース名（Docker で使用）                                                |
| MYSQL_USER           | MySQL のユーザー名（Docker で使用）                                                    |
| MYSQL_PASSWORD       | MySQL のパスワード（Docker で使用）                                                    |
| MYSQL_HOST           | MySQL のホスト名（Docker で使用）                                                      |
| MYSQL_PORT           | MySQL のポート番号（Docker で使用）                                                    |
| PMA_ARBITRARY        | =1 を指定し、ユーザーが phpMyAdmin ログイン時に任意のサーバーに接続できるようにする    |
| PMA_HOST             | phpMyAdmin が接続する MySQL サーバーのホスト名または IP アドレスを指定                 |
| PMA_USER             | phpMyAdmin を使用して MySQL サーバーにアクセスする時に必要な認証情報                   |
| PMA_PASSWORD         | 上記ユーザーのパスワード                                                               |
| OPENAI_API_KEY       | chatGPT トークン                                                                       |

### コマンド一覧

| コマンド                                                     | 実行する処理                                                                                                                  |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| docker compose up                                            | yml ファイルのとおりコンテナ起動（Windows は docker「-」compose）                                                             |
| docker compose stop                                          | コンテナ停止                                                                                                                  |
| docker compose down                                          | コンテナ停止・削除                                                                                                            |
| sh .docker_clear.sh                                          | コンテナ停止・削除、image も全削除                                                                                            |
| docker compose exec django python3 manage.py makemigrations  | Django の model.py を変更したら、migration ファイルを作成                                                                     |
| docker compose exec django python3 manage.py migrate         | Django の migration ファイルをデータベースに反映（注意！：既にデータが何か MySQL に入っていると、反映できずにエラーします。） |
| docker compose exec django python3 manage.py collectstatic   | Django の css ファイルを適用（本番環境ではこれを実行しないと django コンテナの作成でエラーします。）                          |
| docker compose exec django python3 manage.py createsuperuser | Django 管理者用アカウントを作成                                                                                               |
| docker compose run db mysql -u user -p password              | db コンテナに入る                                                                                                             |

<p align="right">(<a href="#top">トップへ</a>)</p>

## トラブルシューティング

<p align="right">(<a href="#top">トップへ</a>)</p>

<br>

## その他

<p align="right">(<a href="#top">トップへ</a>)</p>
