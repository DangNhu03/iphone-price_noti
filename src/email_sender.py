"""Module xử lý gửi email thông báo"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from .config import EMAIL_CONFIG
from .utils import format_price


def _send_raw_email(subject: str, body: str, is_html: bool = True) -> bool:
    """Gửi email thô với subject/body tuỳ ý."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['receiver_email']
        msg['Subject'] = subject

        subtype = 'html' if is_html else 'plain'
        msg.attach(MIMEText(body, subtype, 'utf-8'))

        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        server.send_message(msg)
        server.quit()

        print("Đã gửi email thành công!")
        return True
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")
        return False


def send_email_notification(product_name, product_id, old_price, old_special_price, new_price, new_special_price):
    """Gửi email thông báo khi giá thay đổi"""
    body = f"""
    <html>
    <body>
        <h2>Thông báo thay đổi giá sản phẩm</h2>
        <p><strong>Sản phẩm:</strong> {product_name}</p>
        <p><strong>Mã sản phẩm:</strong> {product_id}</p>
        <hr>
        <h3>Giá cũ:</h3>
        <ul>
            <li>Giá gốc: {format_price(old_price)}</li>
            <li>Giá khuyến mãi: {format_price(old_special_price)}</li>
        </ul>
        <h3>Giá mới:</h3>
        <ul>
            <li>Giá gốc: {format_price(new_price)}</li>
            <li>Giá khuyến mãi: {format_price(new_special_price)}</li>
        </ul>
        <hr>
        <p><small>Thời gian kiểm tra: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</small></p>
    </body>
    </html>
    """
    return _send_raw_email(f"Thông báo thay đổi giá {product_name}", body, is_html=True)


def send_error_notification(error_message: str) -> bool:
    """Gửi email khi có lỗi hệ thống (ví dụ lỗi kết nối database)."""
    subject = "Lỗi hệ thống - iPhone Price Notifier"
    body = f"""Đã xảy ra lỗi trong hệ thống kiểm tra giá:\n\n{error_message}\n\nThời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"""
    return _send_raw_email(subject, body, is_html=False)
