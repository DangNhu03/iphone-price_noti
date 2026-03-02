"""Module chính để kiểm tra và so sánh giá"""

from .api import get_current_price
from .history import load_history, get_product_history, update_product_history
from .email_sender import send_email_notification
from .utils import format_price
from .config import PRODUCTS



def check_price_change():
    """Kiểm tra và so sánh giá cho tất cả sản phẩm"""
    history = load_history()
    
    for product in PRODUCTS:
        product_id = product['product_id']
        product_name = product['product_name']
        province_id = product['province_id']
        
        print(f"\nĐang kiểm tra giá {product_name}...")
        
        # Lấy giá hiện tại
        current_price_data = get_current_price(product_id, province_id)
        
        if current_price_data is None:
            print(f"  Không thể lấy giá từ API!")
            continue
        
        current_price = current_price_data.get('price')
        current_special_price = current_price_data.get('special_price')
        
        print(f"  Giá hiện tại - Gốc: {format_price(current_price)}, Khuyến mãi: {format_price(current_special_price)}")
        
        old_data = get_product_history(history, product_id)
        
        if old_data:
            old_price = old_data.get('price')
            old_special_price = old_data.get('special_price')
            
            price_changed = (old_price != current_price) or (old_special_price != current_special_price)
            
            if price_changed:
                print("  Phát hiện thay đổi giá!")
                print(f"  Giá cũ - Gốc: {format_price(old_price)}, Khuyến mãi: {format_price(old_special_price)}")
                
                send_email_notification(
                    product_name, product_id,
                    old_price, old_special_price,
                    current_price, current_special_price
                )
            else:
                print("  Giá không thay đổi.")
        else:
            print("  Lần đầu kiểm tra, đang lưu giá vào lịch sử...")
        
        # Lưu giá hiện tại vào lịch sử
        history = update_product_history(history, product_id, current_price_data)
    
    print("\nĐã cập nhật lịch sử giá cho tất cả sản phẩm.")

