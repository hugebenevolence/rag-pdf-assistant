# TROUBLESHOOTING.md

# 🚨 Sửa lỗi thường gặp

## ❌ Lỗi: st.session_state.chat_input cannot be modified

**Nguyên nhân**: Streamlit không cho phép thay đổi session state của widget sau khi đã tạo.

**Giải pháp**: Đã sửa trong `app_pro.py` bằng cách:
- Sử dụng `st.form()` để wrap chat input
- Thay đổi logic xử lý quick questions
- Sử dụng `clear_on_submit=True` cho form

## ❌ Lỗi import modules

**Nguyên nhân**: Thiếu dependencies hoặc môi trường chưa được setup.

**Giải pháp**:
```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Hoặc setup toàn bộ môi trường
python setup_dev.py
```

## ❌ Lỗi API Key

**Nguyên nhân**: OPENROUTER_API_KEY chưa được cấu hình.

**Giải pháp**:
1. Mở file `.env`
2. Thay thế `your_openrouter_api_key_here` bằng API key thực
3. Lưu file và restart app

## ❌ Lỗi Memory/Performance

**Nguyên nhân**: File PDF quá lớn hoặc tài nguyên hệ thống không đủ.

**Giải pháp**:
1. Giảm kích thước file PDF (< 50MB)
2. Điều chỉnh chunk_size trong config
3. Restart app để clear cache

## ❌ Lỗi Streamlit khởi động

**Nguyên nhân**: Port đã được sử dụng hoặc Streamlit chưa cài đặt.

**Giải pháp**:
```bash
# Cài đặt Streamlit
pip install streamlit

# Chạy trên port khác
python run_app.py --mode app --port 8502

# Hoặc kill process đang dùng port
netstat -ano | findstr :8501
taskkill /PID <process_id> /F
```

## ❌ Lỗi Docker

**Nguyên nhân**: Docker chưa cài đặt hoặc config sai.

**Giải pháp**:
```bash
# Cài đặt Docker Desktop
# Sau đó chạy:
docker-compose up --build

# Hoặc
docker build -t rag-chatbot .
docker run -p 8501:8501 --env-file .env rag-chatbot
```

## 🔧 Debug Commands

```bash
# Kiểm tra dependencies
python run_app.py --mode check

# Chạy tests
python run_app.py --mode test

# Setup môi trường
python run_app.py --mode setup

# Chạy với debug mode
python run_app.py --mode app --debug
```

## 📞 Support

Nếu vẫn gặp lỗi, hãy:
1. Kiểm tra logs trong thư mục `logs/`
2. Chạy `python run_app.py --mode check` để kiểm tra hệ thống
3. Tạo issue trên GitHub với log đầy đủ
