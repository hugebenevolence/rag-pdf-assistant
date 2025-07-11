# 🎯 Quick Start Guide

## 🚀 Cài đặt nhanh

### 1. Cài đặt Python packages
```bash
pip install -r requirements.txt
```

### 2. Cấu hình API Key
Tạo file `.env` với nội dung:
```
OPENROUTER_API_KEY=your_api_key_here
```

### 3. Chạy ứng dụng
```bash
# Chạy phiên bản Pro (khuyến nghị)
streamlit run app_pro.py

# Hoặc chạy phiên bản cơ bản
streamlit run app.py
```

## 🎮 Demo

```bash
# Chạy demo tương tác
python run_demo.py

# Hoặc setup development environment
python setup_dev.py
```

## 🔧 Tùy chọn chạy

```bash
# Chạy với runner script
python run_app.py --mode app --port 8501

# Chạy demo
python run_app.py --mode demo

# Chạy tests
python run_app.py --mode test
```

## 🐳 Docker

```bash
# Build và chạy với Docker
docker-compose up --build

# Hoặc chạy Docker trực tiếp
docker build -t rag-chatbot .
docker run -p 8501:8501 --env-file .env rag-chatbot
```

## 📖 Sử dụng cơ bản

1. **Tải lên PDF**: Click "Tải lên file PDF" và chọn file
2. **Xử lý tài liệu**: Click "Xử lý tài liệu" và chờ
3. **Đặt câu hỏi**: Nhập câu hỏi và click "Gửi"
4. **Xem kết quả**: Xem câu trả lời và metrics

## 🆘 Troubleshooting

### Lỗi import
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Lỗi API Key
- Kiểm tra file `.env` có tồn tại không
- Đảm bảo API key đúng và có quyền truy cập
- Kiểm tra kết nối internet

### Lỗi memory
- Giảm kích thước file PDF
- Tăng RAM cho hệ thống
- Điều chỉnh chunk_size trong config

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/rag-chatbot/issues)
- **Email**: support@yourcompany.com
