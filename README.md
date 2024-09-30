## 專案說明
 FastAPI 的後端專案，提供用戶驗證、文件上傳和管理等功能。使用 SQLite 作為資料庫，並包含一系列 API 端點來處理用戶和文件的操作。

## 功能介紹
- 用戶驗證
  - 用戶登入
  - Token 驗證
- CRUD 操作
  - 最新消息
  - 社長文告
  - 總監的話
- 數據庫可視化
  - 使用 sqlite-web 來可視化 SQLite 數據庫

## 如何啟動
1. 安裝相關套件
    ### 使用 Poetry 直接安裝
    ```bash
    poetry install
    ```

    ### 轉換成 requirements.txt 進行 pip 安裝
    ```bash
    poetry export -f requirements.txt --output requirements.txt --with dev
    pip install -r requirements.txt
    ```

2. 啟動 FastAPI 應用
    ```bash
    uvicorn app.main:app --port 8000 --reload
    ```

3. 訪問 API 文檔
    在瀏覽器中打開 `http://localhost:8000/docs` 來查看和測試 API 端點。

## 如何可視化 SQLite
1. 啟動 sqlite-web
    ```bash
    python run_sqlite_web.py
    ```

2. 訪問 sqlite-web
    在瀏覽器中打開 `http://localhost:8080` 來查看和管理 SQLite 數據庫。

## 如何運行單元測試
1. 測試檔案目錄
    ```
    ./tests
    ```

2. 運行測試
    ```bash
    pytest -s
    ```
