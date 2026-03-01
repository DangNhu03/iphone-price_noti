# iPhone Price Notification

Dự án tự động kiểm tra giá iPhone trên Cellphones.vn định kì và gửi thông báo qua email khi có thay đổi giá.

## Tính năng

- ✅ Tự động kiểm tra giá sản phẩm từ API Cellphones.vn
- ✅ Lưu lịch sử giá để so sánh
- ✅ Gửi email thông báo khi phát hiện thay đổi giá

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Cấu hình email và sản phẩm trong file `src/config.py`:
   - Điền thông tin email gửi/nhận
   - Điền App Password của Gmail (không dùng mật khẩu thường)
   - Điền ID sản phẩm và tỉnh/thành phố cần kiểm tra

## Sử dụng

Chạy script để kiểm tra giá:
```bash
python main.py
```

## Chạy tự động định kỳ
Sử dụng Github Actions
