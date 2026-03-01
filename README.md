# iPhone Price Notification

Dự án tự động kiểm tra giá iPhone trên Cellphones.vn và gửi thông báo qua email khi có thay đổi giá.

## Tính năng

- ✅ Tự động kiểm tra giá sản phẩm từ API Cellphones.vn
- ✅ Lưu lịch sử giá để so sánh
- ✅ Gửi email thông báo khi phát hiện thay đổi giá
- ✅ Hỗ trợ kiểm tra giá gốc và giá khuyến mãi

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Cấu hình email và sản phẩm trong file `src/config.py`:
   - Điền thông tin email gửi/nhận
   - Điền App Password của Gmail (không dùng mật khẩu thường)
   - Điền ID sản phẩm và tỉnh/thành phố cần kiểm tra

## Cách lấy App Password Gmail

1. Vào [Google Account Settings](https://myaccount.google.com/)
2. Bật 2-Step Verification
3. Vào Security → App passwords
4. Tạo app password mới cho "Mail"
5. Copy password và dán vào `src/config.py`

## Sử dụng

Chạy script để kiểm tra giá:
```bash
python main.py
```

## Chạy tự động định kỳ


## Cấu trúc dự án

```
iphone-price-noti/
├── main.py             # File chính để chạy ứng dụng
├── src/                # Source code
│   ├── __init__.py     # Package init
│   ├── config.py       # File cấu hình
│   ├── api.py          # Xử lý API calls
│   ├── history.py      # Xử lý lịch sử giá
│   ├── email_sender.py  # Xử lý gửi email
│   ├── utils.py        # Các hàm tiện ích
│   └── price_checker.py # Logic chính kiểm tra giá
├── history.json        # Lịch sử giá (tự động tạo)
├── requirements.txt    # Dependencies
└── README.md          # Hướng dẫn
```

## Lưu ý

- File `history.json` sẽ được tạo tự động khi chạy lần đầu
- Đảm bảo cấu hình email đúng để nhận được thông báo
- Có thể chỉnh sửa `PRODUCT_CONFIG` trong `src/config.py` để kiểm tra sản phẩm khác
