# kashi_py

### Open API
```bash
http://localhost:8000/docs#/
```
を確認。

### docker-compose コマンドが失敗する場合
cliかdocker desktopでコンテナを起動すると治る(だいたい)

### イメージのビルド

```bash
docker-compose build
```

### パッケージ管理ツールのインストール
```bash
docker-compose run \
  --entrypoint "poetry init \
    --name demo-app \
    --dependency fastapi \
    --dependency uvicorn[standard]" \
  demo-app
```

### 依存パッケージのインストール
```bash
docker-compose run --entrypoint "poetry install" demo-app
```

### イメージの再ビルド
```bash
docker-compose build --no-cache
```

### サーバ立ち上げ

```bash
docker-compose up
```

### ORMライブラリのインストール

```bash
docker-compose exec demo-app poetry add sqlalchemy aiomysql
```

### DBのtableの初期化

```bash
docker-compose exec demo-app poetry run python -m api.migrate_db
```

### MySQLクライアントの起動

```bash
docker-compose exec db mysql demo
```