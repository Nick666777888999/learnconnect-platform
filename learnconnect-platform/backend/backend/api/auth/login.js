import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';

const JWT_SECRET = process.env.JWT_SECRET || 'learnconnect_secret_2024';

// 模擬用戶數據庫
const users = [
  {
    id: '1',
    name: '管理員',
    email: 'Nick20130104@gmail.com',
    password: '$2a$10$8K1p/a0dRT.7bqGYr5YtgO6Y9Qc7f7Q8qXq9VkLk8b5JzY9W8dO', // Nick20130104
    role: 'admin'
  }
];

export default async function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ error: '方法不允許' });
  }

  try {
    const { email, password } = await request.json();

    // 查找用戶
    const user = users.find(u => u.email === email);
    if (!user) {
      return response.status(401).json({ 
        success: false, 
        message: '電子郵件或密碼錯誤' 
      });
    }

    // 驗證密碼
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      return response.status(401).json({ 
        success: false, 
        message: '電子郵件或密碼錯誤' 
      });
    }

    // 生成 JWT token
    const token = jwt.sign(
      { 
        userId: user.id, 
        email: user.email, 
        role: user.role 
      },
      JWT_SECRET,
      { expiresIn: '24h' }
    );

    response.status(200).json({
      success: true,
      data: {
        user: {
          id: user.id,
          name: user.name,
          email: user.email,
          role: user.role
        },
        token
      },
      message: '登入成功'
    });

  } catch (error) {
    response.status(500).json({ 
      success: false, 
      message: '伺服器錯誤: ' + error.message 
    });
  }
}
