"""Module xử lý lịch sử giá với PostgreSQL (psycopg3)"""

import psycopg
from datetime import datetime
from .config import DATABASE_CONFIG
from .email_sender import send_error_notification


def get_db_connection():
    """Tạo kết nối đến PostgreSQL"""
    try:
        conn = psycopg.connect(
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port'],
            dbname=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
        )
        return conn
    except psycopg.Error as e:
        msg = f"Lỗi kết nối database: {e}"
        print(msg)
        # Thử gửi email báo lỗi, nhưng không để lỗi này phá vỡ luồng chính
        try:
            send_error_notification(msg)
        except Exception:
            pass
        return None


def init_db():
    """Khởi tạo bảng nếu chưa tồn tại"""
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_history (
                id SERIAL PRIMARY KEY,
                product_id VARCHAR(50) NOT NULL UNIQUE,
                price FLOAT,
                special_price FLOAT,
                last_check TIMESTAMP NOT NULL
            );
        """)
        conn.commit()
        print("Database đã sẵn sàng.")
        return True
    except psycopg.Error as e:
        print(f"Lỗi khởi tạo database: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def load_history():
    """Đọc lịch sử giá từ database"""
    conn = get_db_connection()
    if conn is None:
        return {}
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, price, special_price, last_check FROM product_history;")
        rows = cursor.fetchall()
        
        history = {}
        for row in rows:
            product_id, price, special_price, last_check = row
            history[product_id] = {
                'price': price,
                'special_price': special_price,
                'last_check': last_check.isoformat()
            }
        return history
    except psycopg.Error as e:
        print(f"Lỗi khi đọc lịch sử: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()


def save_history(history):
    """Lưu lịch sử giá vào database"""
    # Hàm này không cần thiết nữa vì update_product_history sẽ lưu trực tiếp
    # Nhưng giữ nó để compatibility
    pass


def get_product_history(history, product_id):
    """Lấy lịch sử giá của một sản phẩm"""
    return history.get(product_id)


def update_product_history(history, product_id, price_data):
    """Cập nhật lịch sử giá của một sản phẩm vào database"""
    conn = get_db_connection()
    if conn is None:
        print("Không thể kết nối database, không lưu được lịch sử giá.")
        return history
    
    try:
        cursor = conn.cursor()
        now = datetime.now()
        
        cursor.execute("""
            INSERT INTO product_history (product_id, price, special_price, last_check)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (product_id) 
            DO UPDATE SET 
                price = EXCLUDED.price,
                special_price = EXCLUDED.special_price,
                last_check = EXCLUDED.last_check;
        """, (
            product_id,
            price_data.get('price'),
            price_data.get('special_price'),
            now
        ))
        
        conn.commit()
        
        # Cập nhật history dictionary để giữ consistency
        history[product_id] = {
            'price': price_data.get('price'),
            'special_price': price_data.get('special_price'),
            'last_check': now.isoformat()
        }
        return history
    except psycopg.Error as e:
        print(f"Lỗi khi lưu lịch sử: {e}")
        return history
    finally:
        cursor.close()
        conn.close()

