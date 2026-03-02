"""File chính để chạy ứng dụng"""

from src.price_checker import check_price_change
from src.history import init_db

if __name__ == '__main__':
    # Khởi tạo database
    init_db()
    
    # Chạy kiểm tra giá
    check_price_change()

