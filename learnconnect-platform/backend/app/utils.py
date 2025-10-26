from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.models import db

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = db.get_user_by_id(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({
                'success': False,
                'message': '需要管理員權限'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def create_response(success: bool, data=None, message: str = '', status_code: int = 200):
    response = {
        'success': success,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def error_response(message: str, status_code: int = 400):
    return create_response(False, message=message, status_code=status_code)

def success_response(data=None, message: str = '操作成功'):
    return create_response(True, data=data, message=message)