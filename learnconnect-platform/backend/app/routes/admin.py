from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.utils import success_response, error_response, admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_stats():
    try:
        stats = db.stats.copy()
        
        # 添加管理員專用統計
        admin_stats = {
            **stats,
            'recent_activity': {
                'new_users_today': 150,
                'new_messages_today': 1200,
                'new_resources_today': 85,
                'active_sessions': 4500
            },
            'system_health': {
                'server_uptime': '99.9%',
                'response_time': '125ms',
                'error_rate': '0.05%'
            }
        }
        
        return success_response(
            data={
                'platformStats': admin_stats
            }
        )
        
    except Exception as e:
        return error_response(f'獲取管理員統計失敗: {str(e)}', 500)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_users():
    try:
        users = db.get_all_users()
        users_data = [user.to_dict() for user in users]
        
        # 添加管理員專用字段
        for user_data in users_data:
            user_data['status'] = 'active'
            user_data['last_login'] = user_data.get('last_login', '2024-01-15T10:00:00')
            user_data['login_count'] = 42  # 模擬數據
        
        return success_response(
            data={
                'users': users_data,
                'total': len(users_data)
            }
        )
        
    except Exception as e:
        return error_response(f'獲取用戶管理列表失敗: {str(e)}', 500)

@admin_bp.route('/users/<user_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_user_status(user_id):
    try:
        data = request.get_json()
        if not data:
            return error_response('請求數據不能為空')
        
        status = data.get('status')
        if status not in ['active', 'suspended', 'banned']:
            return error_response('無效的狀態值')
        
        user = db.get_user_by_id(user_id)
        if not user:
            return error_response('用戶不存在', 404)
        
        user.is_active = (status == 'active')
        
        return success_response(
            data={
                'user': user.to_dict()
            },
            message='用戶狀態更新成功'
        )
        
    except Exception as e:
        return error_response(f'更新用戶狀態失敗: {str(e)}', 500)

@admin_bp.route('/content/reports', methods=['GET'])
@jwt_required()
@admin_required
def get_content_reports():
    try:
        # 模擬舉報數據
        reports = [
            {
                'id': '1',
                'type': 'inappropriate_content',
                'reporter_id': 'user_123',
                'target_id': 'message_456',
                'reason': '包含不當語言',
                'status': 'pending',
                'created_at': '2024-01-15T10:00:00'
            },
            {
                'id': '2',
                'type': 'spam',
                'reporter_id': 'user_456',
                'target_id': 'user_789',
                'reason': '發送垃圾訊息',
                'status': 'resolved',
                'created_at': '2024-01-14T15:30:00'
            }
        ]
        
        return success_response(
            data={
                'reports': reports,
                'total': len(reports)
            }
        )
        
    except Exception as e:
        return error_response(f'獲取內容舉報失敗: {str(e)}', 500)

@admin_bp.route('/system/announcements', methods=['POST'])
@jwt_required()
@admin_required
def create_announcement():
    try:
        data = request.get_json()
        if not data:
            return error_response('請求數據不能為空')
        
        title = data.get('title')
        content = data.get('content')
        
        if not title or not content:
            return error_response('請提供標題和內容')
        
        # 模擬創建公告
        announcement = {
            'id': 'announcement_1',
            'title': title,
            'content': content,
            'author_id': get_jwt_identity(),
            'created_at': '2024-01-15T10:00:00',
            'is_published': True
        }
        
        return success_response(
            data=announcement,
            message='公告發布成功'
        ), 201
        
    except Exception as e:
        return error_response(f'發布公告失敗: {str(e)}', 500)