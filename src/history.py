"""Module xử lý lịch sử giá"""

import json
import os
from .config import HISTORY_FILE


def load_history():
    """Đọc lịch sử giá từ file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi khi đọc lịch sử: {e}")
            return {}
    return {}


def save_history(history):
    """Lưu lịch sử giá vào file"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi khi lưu lịch sử: {e}")


def get_product_history(history, product_id):
    """Lấy lịch sử giá của một sản phẩm"""
    return history.get(product_id)


def update_product_history(history, product_id, price_data):
    """Cập nhật lịch sử giá của một sản phẩm"""
    from datetime import datetime
    history[product_id] = {
        'price': price_data.get('price'),
        'special_price': price_data.get('special_price'),
        'last_check': datetime.now().isoformat()
    }
    return history
