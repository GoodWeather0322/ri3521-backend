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
- 資料庫可視化
  - 使用 sqlite-web 來可視化 SQLite 資料庫

## 如何啟動
1. 環境要求
    - Python 3.12
    - poetry (optional)
2. 安裝相關套件
    ### 使用 Poetry 安裝
    ```bash
    poetry install
    ```

    ### 使用 pip 安裝
    ```bash
    pip install -r requirements.txt
    ```

3. 啟動 FastAPI 應用
    ```bash
    uvicorn app.main:app --port 8000 --reload
    ```

4. 訪問 API 文檔
    在瀏覽器中打開 `http://localhost:8000/docs` 來查看和測試 API 端點。

## 如何可視化 SQLite
1. 啟動 sqlite-web
    ```bash
    python run_sqlite_web.py
    ```

2. 訪問 sqlite-web
    在瀏覽器中打開 `http://localhost:8080` 來查看和管理 SQLite 資料庫。

## 如何運行單元測試
1. 測試檔案目錄
    ```
    ./tests
    ```

2. 運行測試
    ```bash
    pytest -s
    ```
