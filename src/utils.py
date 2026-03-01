"""Các hàm tiện ích"""


def format_price(price):
    """Định dạng giá thành VNĐ"""
    if price is None:
        return "N/A"
    return f"{int(price):,} VNĐ"
