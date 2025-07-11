# 🚀 Streamlit Cloud Deployment Guide

## 🛠️ Files đã được chuẩn bị cho deployment

### 1. **requirements.txt** ✅
- Đã thêm `pysqlite3-binary>=0.5.0` để fix SQLite issue
- Đã thêm `faiss-cpu>=1.7.0` như fallback cho ChromaDB
- Tất cả dependencies cần thiết đã được include

### 2. **packages.txt** ✅
```
libsqlite3-dev
sqlite3
```
Cài đặt system packages cho SQLite

### 3. **app_pro.py** ✅
- SQLite fix được áp dụng đầu tiên
- Sử dụng SmartVectorStore (ChromaDB + FAISS fallback)
- Hỗ trợ Streamlit Cloud environment detection

### 4. **.streamlit/config.toml** ✅
- Cấu hình Streamlit tối ưu
- Theme màu đẹp
- Settings phù hợp cho cloud

### 5. **.streamlit/secrets.toml.template** ✅
- Template cho Streamlit secrets
- Hướng dẫn cấu hình API keys

## 📋 Deployment Steps

### 1. **Tải code lên GitHub**
```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### 2. **Cấu hình Streamlit Cloud**
1. Đi tới [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub repository
3. Chọn branch: `main`
4. Main file path: `app_pro.py`

### 3. **Cấu hình Secrets**
Trong Streamlit Cloud dashboard, thêm secrets:
```toml
[api]
OPENROUTER_API_KEY = "your_actual_api_key_here"
```

### 4. **Environment Variables (Optional)**
```toml
[app]
APP_TITLE = "RAG Chatbot Pro"
MAX_FILE_SIZE = 52428800

[llm]
DEFAULT_MODEL = "mistralai/mistral-7b-instruct"
TEMPERATURE = 0.7
MAX_TOKENS = 1024
```

## 🔧 SQLite Fix Details

### Vấn đề
ChromaDB requires SQLite >= 3.35.0, nhưng Streamlit Cloud có version cũ hơn.

### Giải pháp
1. **pysqlite3-binary**: Replacement cho SQLite system
2. **FAISS fallback**: Nếu ChromaDB không hoạt động
3. **Smart detection**: Tự động detect Streamlit Cloud environment

### Code fix trong app_pro.py
```python
# SQLite fix for Streamlit Cloud - MUST BE FIRST
import sys
import os

try:
    if 'STREAMLIT_CLOUD' in os.environ or '/mount/src' in os.getcwd():
        import pysqlite3
        sys.modules['sqlite3'] = pysqlite3
        print("✅ SQLite fix applied for Streamlit Cloud")
except ImportError:
    print("⚠️ pysqlite3 not available, using fallback")
```

## 📊 Vector Store Strategy

### SmartVectorStore Logic:
1. **Try ChromaDB first** - Nếu SQLite fix thành công
2. **Fallback to FAISS** - Nếu ChromaDB không hoạt động
3. **Transparent switching** - App vẫn hoạt động bình thường

## 🔍 Troubleshooting

### Nếu vẫn gặp SQLite error:
1. Kiểm tra `packages.txt` đã được upload
2. Restart deployment
3. Check logs để xem fallback có hoạt động không

### Nếu import error:
1. Kiểm tra `requirements.txt` đầy đủ
2. Rebuild deployment
3. Check Python version compatibility

### Nếu API key error:
1. Kiểm tra secrets configuration
2. Đảm bảo key format đúng
3. Test key locally trước

## ✅ Checklist trước khi deploy:

- [ ] Code đã commit và push lên GitHub
- [ ] OPENROUTER_API_KEY đã chuẩn bị sẵn
- [ ] File `requirements.txt` đã updated
- [ ] File `packages.txt` có trong repo
- [ ] SQLite fix code đã được thêm vào `app_pro.py`
- [ ] SmartVectorStore đã được implement
- [ ] Test local một lần cuối

## 🎉 Expected Result:

Sau khi deploy thành công:
- App sẽ tự động detect Streamlit Cloud
- SQLite issue sẽ được fix tự động
- Nếu ChromaDB không hoạt động, sẽ fallback sang FAISS
- UI sẽ hiển thị đẹp với theme đã config
- Tất cả features sẽ hoạt động bình thường

**Happy Deploying! 🚀**
