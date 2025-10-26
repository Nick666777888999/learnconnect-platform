from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.utils import success_response, error_response

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/rooms/<room_id>/messages', methods=['GET'])
@jwt_required()
def get_chat_messages(room_id):
    try:
        limit = request.args.get('limit', 50, type=int)
        messages = db.get_chat_messages(room_id, limit)
        messages_data = [message.to_dict() for message in messages]
        
        return success_response(
            data=messages_data
        )
        
    except Exception as e:
        return error_response(f'獲取聊天訊息失敗: {str(e)}', 500)

@chat_bp.route('/rooms/<room_id>/messages', methods=['POST'])
@jwt_required()
def send_message(room_id):
    try:
        data = request.get_json()
        if not data:
            return error_response('請求數據不能為空')
        
        content = data.get('content')
        if not content:
            return error_response('訊息內容不能為空')
        
        user_id = get_jwt_identity()
        
        # 發送訊息
        message = db.add_chat_message(room_id, user_id, content)
        
        return success_response(
            data=message.to_dict(),
            message='訊息發送成功'
        ), 201
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f'發送訊息失敗: {str(e)}', 500)

@chat_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_chat_rooms():
    try:
        rooms = db.get_chat_rooms()
        rooms_data = [room.to_dict() for room in rooms]
        
        # 更新成員數量（模擬數據）
        for room in rooms_data:
            room['member_count'] = db.stats['active_users'] // len(rooms_data)
        
        return success_response(
            data=rooms_data
        )
        
    except Exception as e:
        return error_response(f'獲取聊天室列表失敗: {str(e)}', 500)

@chat_bp.route('/rooms/<room_id>', methods=['GET'])
@jwt_required()
def get_chat_room(room_id):
    try:
        rooms = db.get_chat_rooms()
        room = next((r for r in rooms if r.id == room_id), None)
        
        if not room:
            return error_response('聊天室不存在', 404)
        
        room_data = room.to_dict()
        room_data['member_count'] = db.stats['active_users'] // len(rooms)
        
        return success_response(
            data=room_data
        )
        
    except Exception as e:
        return error_response(f'獲取聊天室信息失敗: {str(e)}', 500)

@chat_bp.route('/direct/<user_id>', methods=['POST'])
@jwt_required()
def send_direct_message(user_id):
    try:
        data = request.get_json()
        if not data:
            return error_response('請求數據不能為空')
        
        content = data.get('content')
        if not content:
            return error_response('訊息內容不能為空')
        
        current_user_id = get_jwt_identity()
        target_user = db.get_user_by_id(user_id)
        
        if not target_user:
            return error_response('目標用戶不存在', 404)
        
        # 創建或獲取私聊房間（這裡簡化處理）
        room_id = f'direct_{min(current_user_id, user_id)}_{max(current_user_id, user_id)}'
        
        # 發送訊息
        message = db.add_chat_message(room_id, current_user_id, content)
        
        return success_response(
            data=message.to_dict(),
            message='私訊發送成功'
        ), 201
        
    except Exception as e:
        return error_response(f'發送私訊失敗: {str(e)}', 500)