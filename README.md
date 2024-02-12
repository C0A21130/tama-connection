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
このアプリはPythonを使ったWebアプリです。投稿された写真の位置情報やタグ、タイトルなどのメタデータをDBに保存やフロントエンドに送信などをREST APIのルールに従って行います。より詳しいAPIの仕様はOPEN APIを確認してください。
![architecture](https://github.com/C0A21130/tama-connection/assets/85671824/d54186e1-9312-4ed6-a543-6a40ce9e7ae1)

### 利用した言語やライブラリ
- Python
    - FastAPI
    - uvicorn
    - SQLAlchemy
    - PyMySQL
    - PyJWT
    - pytest
- MySQL
- Docker
    - docker-compose

### ディレクトリ構成
``` shell
tama-connection
├─app
|  ├─lib
|  |  ├─map.py：
|  |  ├─page.py：投稿(投稿された内容の確認・投稿をDBに保存・投稿された内容の削除など)に関する機能
|  |  ├─pint.py：いいね機能
|  |  └─user.py：ユーザー(登録・ログイン)に関する機能
|  ├─database.py：データベースへ接続する機能
|  ├─main.py：APIサーバーのリクエストを振り分けてメソッドを呼び出す
|  ├─model.py：リクエストボディの型やSQLの型を定義する
|  └─test.py：テストコード
├─mysql
|  ├─docker-compose.yml：MySQLサーバーのコンテナに関する設定
|  ├─Dockerfile：MySQLサーバーのコンテナに関する設定
|  └─my.cnf：MySQLの設定ファイル
├─.env.sample：設定ファイルのテンプレート(MySQLの接続設定・JWTKEYを書き込む)
├─.gitnore
├─docker-compose.yml：FastAPIサーバーのコンテナを設定
├─Dockerfile：FastAPIサーバーのコンテナを設定
├─openapi.yaml：APIの仕様書
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
3. 環境変数の設定
    - テンプレートファイル(.env.sample)をコピーして.envファイルの中身を書き換える
``` shell
$ cp ./.env.sample ./app/.env
```
4. Dockerのコンテナを起動する
    - MySQLサーバーのコンテナを起動
    - Fast APIサーバーのコンテナを起動
``` shell
$ cd mysql
$ docker-compose up -d
```    
``` shell
$ cd ..
$ docker-compose up -d
```
5. バックエンドサーバーへアクセスする
    - バックエンドサーバー：[http://localhost:5000](http://localhost:5000)

