import os
import subprocess

if __name__ == "__main__":
    # 獲取資料庫檔案路徑
    database_path = os.path.join(os.path.dirname(__file__), "sql_app.db")
    # 啟動 sqlite-web
    subprocess.run(["sqlite_web", database_path, "--port", "8080"])
