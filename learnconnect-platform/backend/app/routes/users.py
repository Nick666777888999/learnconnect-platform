from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.utils import success_response, error_response, admin_required

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = db.get_all_users()
        users_data = [user.to_dict() for user in users]
        
        return success_response(
            data={
                'users': users_data,
                'total': len(users_data)
            }
        )
        
    except Exception as e:
        return error_response(f'獲取用戶列表失敗: {str(e)}', 500)

@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
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

@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = db.get_user_by_id(current_user_id)
        
        # 檢查權限：只能修改自己的資料或管理員
        if current_user_id != user_id and current_user.role != 'admin':
            return error_response('沒有權限修改此用戶資料', 403)
        
        user = db.get_user_by_id(user_id)
        if not user:
            return error_response('用戶不存在', 404)
        
        data = request.get_json()
        if not data:
            return error_response('請求數據不能為空')
        
        # 更新用戶資料
        if 'name' in data:
            user.name = data['name']
        
        return success_response(
            data={
                'user': user.to_dict()
            },
            message='用戶資料更新成功'
        )
        
    except Exception as e:
        return error_response(f'更新用戶資料失敗: {str(e)}', 500)

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        user_id = get_jwt_identity()
        user = db.get_user_by_id(user_id)
        
        if not user:
            return error_response('用戶不存在', 404)
        
        # 這裡可以添加更多的用戶資料
        profile_data = {
            **user.to_dict(),
            'learning_stats': {
                'completed_courses': 12,
                'study_hours': 35,
                'skills_mastered': 8,
                'progress': 75
            },
            'recent_activity': [
                {'type': 'course_complete', 'title': '微積分基礎', 'date': '2024-01-15'},
                {'type': 'resource_share', 'title': '學習筆記分享', 'date': '2024-01-14'},
                {'type': 'group_join', 'title': '加入數學討論組', 'date': '2024-01-13'}
            ]
        }
        
        return success_response(
            data={
                'profile': profile_data
            }
        )
        
    except Exception as e:
        return error_response(f'獲取用戶檔案失敗: {str(e)}', 500)