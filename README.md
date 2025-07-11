# 🚀 RAG Chatbot Pro

Một hệ thống chatbot RAG (Retrieval-Augmented Generation) hiện đại và mạnh mẽ, được thiết kế đặc biệt cho tài liệu tiếng Việt.

## ✨ Tính năng nổi bật

### 🎯 Core Features
- **📚 Xử lý PDF thông minh**: Semantic chunking với mô hình embedding tiếng Việt
- **🤖 Multi-LLM Support**: Hỗ trợ nhiều mô hình AI qua OpenRouter
- **🧠 Memory cuộc trò chuyện**: Ghi nhớ ngữ cảnh để trò chuyện tự nhiên
- **⚡ Streaming Response**: Hiển thị câu trả lời theo thời gian thực
- **🎨 UI/UX hiện đại**: Giao diện đẹp mắt và responsive

### 🔧 Advanced Features
- **📊 Real-time Metrics**: Theo dõi hiệu suất hệ thống
- **💾 Smart Caching**: Tăng tốc xử lý với cache thông minh
- **📝 Comprehensive Logging**: Ghi log chi tiết cho debug
- **🌡️ Configurable Parameters**: Tùy chỉnh temperature, tokens, v.v.
- **📈 Analytics Dashboard**: Biểu đồ thống kê trực quan

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/yourusername/rag-chatbot-pro.git
cd rag-chatbot-pro
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment
Tạo file `.env` với nội dung:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 5. Chạy ứng dụng
```bash
# Chạy phiên bản Pro (khuyến nghị)
streamlit run app_pro.py

# Hoặc chạy phiên bản cơ bản
streamlit run app.py
```

## 🏗️ Cấu trúc Project

```
RAG_Chatbot/
├── app.py                 # Ứng dụng Streamlit cơ bản
├── app_pro.py            # Ứng dụng Streamlit Pro với UI hiện đại
├── config.py             # Cấu hình tập trung
├── requirements.txt      # Dependencies
├── .env                  # Environment variables
├── modules/              # Core modules
│   ├── pdf_processor.py  # Xử lý PDF và chunking
│   ├── vector_store.py   # Vector database
│   ├── llm_wrapper.py    # LLM integration
│   └── rag_pipeline.py   # RAG pipeline với memory
├── utils/                # Utilities
│   ├── logger.py         # Custom logging
│   ├── cache.py          # Caching system
│   ├── metrics.py        # Metrics collector
│   └── __init__.py
├── logs/                 # Log files
├── cache/                # Cache storage
└── docs/                 # Documentation
```

## 🔧 Cấu hình

### Model Support
- **mistralai/mistral-7b-instruct** (mặc định)
- **meta-llama/llama-2-7b-chat**
- **google/gemma-7b-it**
- **microsoft/DialoGPT-medium**

### Embedding Model
- **bkai-foundation-models/vietnamese-bi-encoder** (tối ưu cho tiếng Việt)

### Chunking Strategy
- **Semantic Chunking**: Chia văn bản dựa trên ngữ nghĩa
- **Configurable**: Tùy chỉnh chunk size, overlap, threshold

## 🚀 Cách sử dụng

### 1. Tải lên tài liệu
- Hỗ trợ file PDF (tối đa 50MB)
- Xử lý tự động và hiển thị progress

### 2. Trò chuyện
- Đặt câu hỏi bằng tiếng Việt
- Hệ thống tự động tìm kiếm và trả lời
- Hỗ trợ streaming response

### 3. Tùy chỉnh
- Điều chỉnh temperature cho độ sáng tạo
- Chọn model AI phù hợp
- Bật/tắt memory cuộc trò chuyện

### 4. Theo dõi
- Xem metrics real-time
- Phân tích thời gian phản hồi
- Xuất báo cáo JSON

## 📊 Metrics & Analytics

### Metrics được theo dõi:
- **Questions Asked**: Số câu hỏi đã được hỏi
- **Documents Processed**: Số tài liệu đã xử lý
- **Average Response Time**: Thời gian phản hồi trung bình
- **Total Chunks**: Tổng số chunks được tạo
- **Error Rate**: Tỷ lệ lỗi

### Analytics Dashboard:
- **Response Time Chart**: Biểu đồ thời gian phản hồi
- **Usage Statistics**: Thống kê sử dụng
- **Performance Metrics**: Chỉ số hiệu suất

## 🔍 Advanced Usage

### Custom Configuration
```python
from config import app_config

# Tùy chỉnh cấu hình
app_config.temperature = 0.5
app_config.max_tokens = 2048
app_config.chunk_size = 1500
```

### Programmatic API
```python
from modules.pdf_processor import PDFProcessor
from modules.vector_store import VectorStore
from modules.llm_wrapper import LLMWrapper
from modules.rag_pipeline import RAGPipeline

# Khởi tạo pipeline
processor = PDFProcessor()
chunks = processor.load_and_chunk("document.pdf")

vector_store = VectorStore(processor.embedding_model)
retriever = vector_store.build_store(chunks)

llm = LLMWrapper().get_llm()
pipeline = RAGPipeline(retriever, llm)

# Trò chuyện
answer = pipeline.ask("Tài liệu này nói về gì?")
print(answer)
```

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **Import Error**: Đảm bảo đã cài đặt đúng dependencies
2. **API Key Error**: Kiểm tra file `.env` và API key
3. **Memory Error**: Giảm chunk size hoặc tăng RAM
4. **Model Loading Error**: Kiểm tra kết nối internet

### Debug Mode:
```bash
# Chạy với debug mode
streamlit run app_pro.py --logger.level=debug
```

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain**: Framework for LLM applications
- **Streamlit**: Web app framework
- **OpenRouter**: LLM API provider
- **BKAI**: Vietnamese embedding model
- **Chroma**: Vector database

## 📞 Support

- **Email**: nhantd.dev@gmail.com
- **Issues**: [GitHub Issues](https://github.com/hugebenevolence/rag-pdf-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hugebenevolence/rag-pdf-assistant/discussions)

---

## 🎯 Roadmap

### Version 2.0
- [ ] Multi-document support
- [ ] OCR integration
- [ ] Voice input/output
- [ ] API endpoints
- [ ] Docker containerization

### Version 2.1
- [ ] Database integration
- [ ] User authentication
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] Export to various formats

---

**Made with ❤️ by [Your Team]**
