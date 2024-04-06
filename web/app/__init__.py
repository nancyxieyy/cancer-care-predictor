from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    app.secret_key = 'your_secret_key'  # 设置一个安全密钥
    load_dotenv()  # 确保这行代码在创建 Flask 应用实例之前

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
