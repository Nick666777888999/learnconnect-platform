from flask import Blueprint
from app.models import db
from app.utils import success_response, error_response

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats', methods=['GET'])
def get_platform_stats():
    try:
        return success_response(
            data=db.stats
        )
        
    except Exception as e:
        return error_response(f'獲取平台統計失敗: {str(e)}', 500)

@stats_bp.route('/health', methods=['GET'])
def health_check():
    try:
        return success_response(
            data={
                'status': 'healthy',
                'timestamp': '2024-01-15T10:00:00Z',
                'version': '1.0.0',
                'environment': 'production'
            },
            message='服務正常運行'
        )
        
    except Exception as e:
        return error_response(f'健康檢查失敗: {str(e)}', 500)