from flask import Flask
# from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    load_dotenv()  # 确保这行代码在创建 Flask 应用实例之前

    #app.secret_key = 'your_secret_key'  # 设置一个安全密钥
    app.secret_key = os.getenv('SECRET_KEY')
    
    # 配置MySQL
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_PASSWORD'] = 'yy020529'
    # app.config['MYSQL_DB'] = 'user_db'

    # mysql = MySQL(app)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app