export default function handler(request, response) {
  response.status(200).json({
    success: true,
    data: {
      total_users: 50000,
      total_groups: 1200,
      total_resources: 15000,
      active_users: 15000,
      satisfaction_rate: 98
    }
  });
}
