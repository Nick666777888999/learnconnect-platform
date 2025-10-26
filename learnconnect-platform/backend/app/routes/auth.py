from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db
from app.utils import success_response, error_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return error_response('請求數據不能為空')
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return error_response('請提供電子郵件和密碼')
        
        # 查找用戶
        user = db.get_user_by_email(email)
        if not user:
            return error_response('電子郵件或密碼錯誤', 401)
        
        # 驗證密碼
        if not user.check_password(password):
            return error_response('電子郵件或密碼錯誤', 401)
        
        # 檢查用戶是否激活
        if not user.is_active:
            return error_response('帳號已被停用', 403)
        
        # 更新最後登入時間
        db.update_user_last_login(user.id)
        
        # 創建訪問令牌
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'email': user.email,
                'role': user.role,
                'name': user.name
            }
        )
        
        return success_response(
            data={
                'user': user.to_dict(),
                'token': access_token
            },
            message='登入成功'
        )
        
    except Exception as e:
        return error_response(f'登入失敗: {str(e)}', 500)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return error_response('請求數據不能為空')
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return error_response('請提供姓名、電子郵件和密碼')
        
        if len(password) < 6:
            return error_response('密碼長度至少為6個字符')
        
        # 創建用戶
        user = db.create_user(name, email, password)
        
        # 創建訪問令牌
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'email': user.email,
                'role': user.role,
                'name': user.name
            }
        )
        
        return success_response(
            data={
                'user': user.to_dict(),
                'token': access_token
            },
            message='註冊成功'
        ), 201
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f'註冊失敗: {str(e)}', 500)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return success_response(message='登出成功')

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        user_id = get_jwt_identity()
        user = db.get_user_by_id(user_id)
        
        if not user:
            return error_response('用戶不存在', 404)
        
        return success_response(
            data={
                'user': user.to_dict()
            }
        )
        
    except Exception as e:
        return error_response(f'驗證失敗: {str(e)}', 500)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = db.get_user_by_id(user_id)
        
        if not user:
            return error_response('用戶不存在', 404)
        
        return success_response(
            data={
                'user': user.to_dict()
            }
        )
        
    except Exception as e:
        return error_response(f'獲取用戶信息失敗: {str(e)}', 500)