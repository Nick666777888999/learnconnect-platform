export default function handler(request, response) {
  response.status(200).json({
    status: 'success',
    message: 'LearnConnect API 運行中 🚀',
    timestamp: new Date().toISOString(),
    endpoints: {
      '/api/auth/login': 'POST - 用戶登入',
      '/api/auth/register': 'POST - 用戶註冊',
      '/api/chat/rooms': 'GET - 聊天室列表',
      '/api/stats': 'GET - 平台統計',
      '/api/admin/users': 'GET - 用戶管理'
    },
    admin_account: {
      email: 'Nick20130104@gmail.com',
      password: 'Nick20130104'
    }
  });
}
