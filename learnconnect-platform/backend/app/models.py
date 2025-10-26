import uuid
from datetime import datetime, timedelta
import bcrypt
from typing import Dict, List, Optional

class User:
    def __init__(self, user_id: str, name: str, email: str, password_hash: str, role: str = 'user'):
        self.id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = datetime.utcnow()
        self.last_login = None
        self.is_active = True
        
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

class ChatMessage:
    def __init__(self, message_id: str, room_id: str, user_id: str, content: str, message_type: str = 'user'):
        self.id = message_id
        self.room_id = room_id
        self.user_id = user_id
        self.content = content
        self.type = message_type
        self.timestamp = datetime.utcnow()
        
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'room_id': self.room_id,
            'user_id': self.user_id,
            'content': self.content,
            'type': self.type,
            'timestamp': self.timestamp.isoformat()
        }

class ChatRoom:
    def __init__(self, room_id: str, name: str, description: str = ''):
        self.id = room_id
        self.name = name
        self.description = description
        self.created_at = datetime.utcnow()
        self.member_count = 0
        
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'member_count': self.member_count,
            'created_at': self.created_at.isoformat()
        }

# 模擬數據庫
class Database:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.chat_messages: Dict[str, List[ChatMessage]] = {}
        self.chat_rooms: Dict[str, ChatRoom] = {}
        self.stats = {
            'total_users': 50000,
            'total_groups': 1200,
            'total_resources': 15000,
            'active_users': 15000
        }
        self._initialize_data()
    
    def _initialize_data(self):
        # 初始化管理員用戶
        admin_password = bcrypt.hashpw('Nick20130104'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = User(
            user_id='1',
            name='管理員',
            email='Nick20130104@gmail.com',
            password_hash=admin_password,
            role='admin'
        )
        self.users[admin_user.id] = admin_user
        
        # 初始化聊天室
        general_room = ChatRoom('general', '一般聊天室', '歡迎所有用戶的公開聊天室')
        math_room = ChatRoom('math', '數學討論區', '數學學習與問題討論')
        science_room = ChatRoom('science', '科學討論區', '科學知識分享與討論')
        
        self.chat_rooms[general_room.id] = general_room
        self.chat_rooms[math_room.id] = math_room
        self.chat_rooms[science_room.id] = science_room
        
        # 初始化聊天訊息
        welcome_message = ChatMessage(
            message_id=str(uuid.uuid4()),
            room_id='general',
            user_id='1',
            content='歡迎來到 LearnConnect！',
            message_type='system'
        )
        
        if 'general' not in self.chat_messages:
            self.chat_messages['general'] = []
        self.chat_messages['general'].append(welcome_message)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    def create_user(self, name: str, email: str, password: str) -> User:
        # 檢查郵箱是否已存在
        if self.get_user_by_email(email):
            raise ValueError('該電子郵件已被註冊')
        
        # 哈希密碼
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 確定用戶角色
        role = 'student' if email.endswith('@stu.kcislk.ntpc.edu.tw') else 'user'
        
        # 創建用戶
        user_id = str(uuid.uuid4())
        user = User(user_id, name, email, password_hash, role)
        self.users[user_id] = user
        
        # 更新統計
        self.stats['total_users'] += 1
        
        return user
    
    def add_chat_message(self, room_id: str, user_id: str, content: str) -> ChatMessage:
        if room_id not in self.chat_rooms:
            raise ValueError('聊天室不存在')
        
        message_id = str(uuid.uuid4())
        message = ChatMessage(message_id, room_id, user_id, content)
        
        if room_id not in self.chat_messages:
            self.chat_messages[room_id] = []
        
        self.chat_messages[room_id].append(message)
        return message
    
    def get_chat_messages(self, room_id: str, limit: int = 50) -> List[ChatMessage]:
        if room_id not in self.chat_messages:
            return []
        
        messages = self.chat_messages[room_id]
        return sorted(messages, key=lambda x: x.timestamp)[-limit:]
    
    def get_chat_rooms(self) -> List[ChatRoom]:
        return list(self.chat_rooms.values())
    
    def get_all_users(self) -> List[User]:
        return list(self.users.values())
    
    def update_user_last_login(self, user_id: str):
        user = self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()

# 全局數據庫實例
db = Database()