"""Load .env for local dev (optional)"""
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import os

# Cấu hình email - đọc từ biến môi trường (GitHub Actions) hoặc .env (local)
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'sender_email': os.getenv('EMAIL_SENDER', ''),
    'sender_password': os.getenv('EMAIL_PASSWORD', ''),
    'receiver_email': os.getenv('EMAIL_RECEIVER', ''),
}

# Danh sách sản phẩm cần theo dõi giá
PRODUCTS = [
    {
        'product_id': '68894',
        'province_id': 30,
        'product_name': 'iPhone 15 Black',
    },
    {
        'product_id': '68874',
        'province_id': 30,
        'product_name': 'iPhone 15 Pro Titan tự nhiên 128GB',
    },
    {
        'product_id': '68917',
        'province_id': 30,
        'product_name': 'iPhone 15 Pro Max Titan black 256GB',
    },
]

# API endpoint
API_URL = 'https://api.cellphones.com.vn/v2/graphql/query'

# File lưu lịch sử giá
HISTORY_FILE = 'history.json'
