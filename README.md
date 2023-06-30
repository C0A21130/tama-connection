# たまこねくしょん(バックエンド)

![package](https://img.shields.io/github/stars/C0A21130/tama-connection?style=social)  
![Packages](https://img.shields.io/github/languages/code-size/C0A21130/tama-connection)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/C0A21130/tama-connection)

たまこねくしょんとは、東京工科大学コンピュータサイエンス学部が多摩地域を、ITサービスを使って活性化を行うために活動を行っています。これはWebアプリのバックエンド側のコードを管理するリポジトリです。[アプリはこちらのリンク](https://tama-connect.com)から利用できます。
[フロントエンドのレポジトリ](https://github.com/C0A21130/Tama-connection-front)はこちらです。  
![サムネイル](https://user-images.githubusercontent.com/85671824/225310148-336a8c4c-87a3-43ec-ba97-315d016dc773.png)

## 目次
- アプリの説明
- アプリの機能
    - 投稿関連の機能
    - マップ機能
    - ユーザー管理機能
    - いいね機能
- 技術の仕様
    - 利用した言語とライブラリ
    - ディレクトリ構成
- 使い方
    - テスト方法
    - デプロイ方法

## アプリの説明
このアプリは多摩地域でより楽しく生活できるようにするSNS型アプリです。主な機能はタグ(たまファーム、グルメ、たまさんぽ、お土産)から写真を検索できます。さらに自分の行った場所から多摩地域の写真を投稿できます。

## アプリの機能
### 投稿関連の機能
- 一つの投稿情報をDBから取得する
- 複数の投稿情報をDBから取得する
- 投稿された内容をDBに保存する
- 投稿された内容をDBから削除する

### マップ機能
- 地区名で検索する
- 近くの場所で投稿された情報を検索する

### ユーザー管理機能
- ユーザー情報を登録してJWTを生成する
- JWTからユーザーIDを取得する
- ユーザー情報を削除する
- パスワードの情報を変更する

### いいね機能
- いいね
- 行きたいと思った
- 行ったことがある

## 技術の仕様
このアプリはPythonを使ったWebアプリです。投稿された写真の位置情報やタグ、タイトルなどのメタデータをDBに保存やフロントエンドに送信などをREST APIのルールに従って行います。より詳しいAPIの仕様はOPENAPIを確認してください。
![azure drawio](https://github.com/C0A21130/tama-connection/assets/85671824/bb694f76-a3f6-48e8-abb3-35aa5f2c6a9b)

### 利用した言語やライブラリ
- Python
    - FastAPI
    - uvicorn
    - pymongo
    - jwt
- MongoDB
- Docker
    - docker-compose

### ディレクトリ構成
``` shell
tama-connection
├──app
|   ├─database.py：データベースへ接続する
|   ├─main.py：APIサーバーのリクエストを振り分けてメソッドを呼び出す
|   ├─model.py：型を定義する
|   ├─page.py：投稿(投稿された内容の確認・投稿をDBに保存・投稿された内容の削除など)に関する機能
|   ├─pint.py：いいね機能
|   └─user.py：ユーザー(登録・ログイン)に関する
├─.gitnore
├─Dockerfile：Dockerに関する設定
├─docker-compose.yml：複数のコンテナを設定
├─openapi.yaml：APIの定義
├─README.md
└─requirements.txt：Pythonのライブラリを定義
```

## 使い方
### テスト方法
1. GitHubからリポジトリをクローン
``` shell
$ git clone https://github.com/C0A21130/tama-connection.git
```
2. ブランチを変更
``` shell
$ git switch Develop
```
3. Dockerのコンテナを起動する
``` shell
$ docker-compose up -d
```
4. バックエンドサーバーへアクセスする
    - バックエンドサーバー：[http://localhost:5000](http://localhost:5000)
    - DBサーバー：[http://localhost:8081](http://localhost:8081)


### デプロイ方法
1. GitHubからリポジトリをクローン
``` shell
$ git clone https://github.com/C0A21130/tama-connection.git
```
2. Pythonのライブラリのインストール
``` shell
$ pip install -r requirements.txt
```
3. ディレクトリを変更する
``` shell
$ cd app
```
4. アプリを起動する
``` shell
$ python3 main.py
```
5. アプリへアクセスする
