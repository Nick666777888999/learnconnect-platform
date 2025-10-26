export default function handler(request, response) {
  const rooms = [
    {
      id: 'general',
      name: '一般聊天室',
      description: '歡迎所有用戶的公開聊天室',
      member_count: 15000,
      created_at: '2024-01-01T00:00:00Z'
    },
    {
      id: 'math',
      name: '數學討論區', 
      description: '數學學習與問題討論',
      member_count: 3000,
      created_at: '2024-01-01T00:00:00Z'
    },
    {
      id: 'science',
      name: '科學討論區',
      description: '科學知識分享與討論',
      member_count: 2500,
      created_at: '2024-01-01T00:00:00Z'
    }
  ];

  response.status(200).json({
    success: true,
    data: rooms
  });
}
