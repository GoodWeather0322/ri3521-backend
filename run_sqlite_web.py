import os
import subprocess

if __name__ == "__main__":
    # 获取数据库文件路径
    database_path = os.path.join(os.path.dirname(__file__), "sql_app.db")
    # 启动 sqlite-web
    subprocess.run(["sqlite_web", database_path, "--port", "8080"])
