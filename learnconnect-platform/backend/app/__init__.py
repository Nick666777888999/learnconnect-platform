from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'learnconnect_secret_key_2024')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'learnconnect_jwt_secret_2024')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24小時
    
    # 初始化擴展
    CORS(app)
    jwt = JWTManager(app)
    
    # 註冊藍圖
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.chat import chat_bp
    from app.routes.admin import admin_bp
    from app.routes.stats import stats_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(stats_bp, url_prefix='/api')
    
    return app