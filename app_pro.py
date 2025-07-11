# app_pro.py

# SQLite fix for Streamlit Cloud - MUST BE FIRST
import sys
import os

# Fix SQLite version for ChromaDB on Streamlit Cloud
try:
    # Check if we're on Streamlit Cloud or similar environment
    if 'STREAMLIT_CLOUD' in os.environ or 'streamlit' in sys.modules or os.path.exists('/mount/src'):
        try:
            import pysqlite3
            sys.modules['sqlite3'] = pysqlite3
            print("✅ SQLite fix applied for Streamlit Cloud")
        except ImportError:
            print("⚠️ pysqlite3 not available, using system sqlite3")
except Exception as e:
    print(f"⚠️ SQLite fix warning: {e}")

import streamlit as st
import tempfile
import os
import time
import plotly.graph_objects as go
import plotly.express as px
from typing import Generator
import json

# Import các module đã cải tiến
from modules.pdf_processor import PDFProcessor
from modules.vector_store_fallback import SmartVectorStore
from modules.llm_wrapper import LLMWrapper
from modules.rag_pipeline import RAGPipeline
from config import app_config
from utils.logger import get_logger
from utils.metrics import get_metrics

# Cấu hình trang
st.set_page_config(
    page_title=app_config.app_title,
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/rag-chatbot',
        'Report a bug': "https://github.com/yourusername/rag-chatbot/issues",
        'About': "RAG Chatbot Pro - Powered by AI"
    }
)

# Custom CSS để làm đẹp giao diện
st.markdown("""
<style>
    /* Main background and theme */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styles */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Card styles */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .upload-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        text-align: center;
    }
    
    .chat-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        min-height: 400px;
    }
    
    .metrics-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    }
    
    /* Button styles */
    .stButton button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Chat message styles */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        margin-right: 20%;
    }
    
    /* Sidebar styles */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* Progress bar */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metrics display */
    .metric-container {
        background: rgba(255,255,255,0.9);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2rem; }
        .main-header p { font-size: 1rem; }
        .card { padding: 1rem; }
        .user-message, .bot-message { margin-left: 0; margin-right: 0; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize logger và metrics
logger = get_logger()
metrics = get_metrics()

# Initialize session states
def init_session_state():
    """Khởi tạo session state"""
    if "retriever" not in st.session_state:
        st.session_state.retriever = None
    if "rag_pipeline" not in st.session_state:
        st.session_state.rag_pipeline = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "document_processed" not in st.session_state:
        st.session_state.document_processed = False
    if "current_doc_info" not in st.session_state:
        st.session_state.current_doc_info = {}
    if "processing_status" not in st.session_state:
        st.session_state.processing_status = ""
    if "selected_question" not in st.session_state:
        st.session_state.selected_question = None

init_session_state()

# Header
st.markdown("""
<div class="main-header fade-in">
    <h1>📚 RAG Chatbot Pro</h1>
    <p>Trò chuyện thông minh với tài liệu PDF bằng AI - Hỗ trợ tiếng Việt</p>
    <p>🚀 Tính năng mới: Memory cuộc trò chuyện • Streaming response • Metrics real-time</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Cấu hình")
    
    # Model selection
    model_options = [
        "mistralai/mistral-7b-instruct",
        "meta-llama/llama-2-7b-chat",
        "google/gemma-7b-it",
        "microsoft/DialoGPT-medium"
    ]
    
    selected_model = st.selectbox(
        "🤖 Chọn Model AI:",
        model_options,
        index=0,
        help="Chọn model AI để trò chuyện"
    )
    
    # Temperature slider
    temperature = st.slider(
        "🌡️ Độ sáng tạo (Temperature):",
        min_value=0.1,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Càng cao càng sáng tạo, càng thấp càng chính xác"
    )
    
    # Max tokens slider
    max_tokens = st.slider(
        "📝 Độ dài tối đa câu trả lời:",
        min_value=256,
        max_value=2048,
        value=1024,
        step=128,
        help="Số token tối đa cho mỗi câu trả lời"
    )
    
    # Use memory checkbox
    use_memory = st.checkbox(
        "🧠 Sử dụng Memory cuộc trò chuyện",
        value=True,
        help="Ghi nhớ ngữ cảnh cuộc trò chuyện"
    )
    
    # Streaming checkbox
    use_streaming = st.checkbox(
        "⚡ Streaming response",
        value=True,
        help="Hiển thị câu trả lời theo thời gian thực"
    )
    
    st.markdown("---")
    
    # Current metrics
    if st.session_state.rag_pipeline:
        st.markdown("## 📊 Metrics")
        current_metrics = metrics.get_metrics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Câu hỏi", current_metrics.get("questions_asked", 0))
            st.metric("Tài liệu", current_metrics.get("documents_processed", 0))
        
        with col2:
            avg_time = current_metrics.get("average_response_time", 0)
            st.metric("Thời gian TB", f"{avg_time:.2f}s")
            st.metric("Errors", current_metrics.get("errors", 0))
    
    st.markdown("---")
    
    # Actions
    if st.button("🗑️ Xóa lịch sử chat"):
        st.session_state.chat_history = []
        if st.session_state.rag_pipeline:
            st.session_state.rag_pipeline.clear_memory()
        st.success("Đã xóa lịch sử!")
        st.rerun()
    
    if st.button("📊 Xuất báo cáo"):
        if st.session_state.rag_pipeline:
            report_data = {
                "metrics": metrics.get_metrics(),
                "chat_history": st.session_state.chat_history,
                "document_info": st.session_state.current_doc_info,
                "pipeline_info": st.session_state.rag_pipeline.get_pipeline_info()
            }
            
            st.download_button(
                label="📥 Tải báo cáo JSON",
                data=json.dumps(report_data, indent=2, ensure_ascii=False),
                file_name=f"rag_report_{int(time.time())}.json",
                mime="application/json"
            )

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card upload-card fade-in">', unsafe_allow_html=True)
    st.markdown("## 📤 Tải lên tài liệu")
    
    uploaded_file = st.file_uploader(
        "Chọn file PDF để phân tích:",
        type=["pdf"],
        help=f"Kích thước tối đa: {app_config.max_file_size // (1024*1024)}MB"
    )
    
    if uploaded_file:
        # Hiển thị thông tin file
        file_size = len(uploaded_file.read())
        uploaded_file.seek(0)  # Reset file pointer
        
        st.info(f"📄 **{uploaded_file.name}**")
        st.info(f"📏 Kích thước: {file_size / (1024*1024):.2f} MB")
        
        if st.button("⚙️ Xử lý tài liệu", type="primary"):
            if file_size > app_config.max_file_size:
                st.error(f"File quá lớn! Kích thước tối đa: {app_config.max_file_size // (1024*1024)}MB")
            else:
                # Processing animation
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Lưu file tạm
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    
                    # Xử lý từng bước với progress bar
                    status_text.text("🔄 Đang khởi tạo processor...")
                    progress_bar.progress(20)
                    
                    processor = PDFProcessor()
                    
                    status_text.text("📖 Đang đọc và chia nhỏ tài liệu...")
                    progress_bar.progress(40)
                    
                    chunks = processor.load_and_chunk(tmp_path)
                    
                    status_text.text("🔍 Đang xây dựng vector store...")
                    progress_bar.progress(60)
                    
                    vector = SmartVectorStore(processor.embedding_model)
                    retriever = vector.build_store(chunks)
                    
                    status_text.text("🤖 Đang khởi tạo LLM...")
                    progress_bar.progress(80)
                    
                    llm = LLMWrapper(model_name=selected_model).get_llm()
                    
                    status_text.text("🔗 Đang tạo RAG pipeline...")
                    progress_bar.progress(90)
                    
                    pipeline = RAGPipeline(retriever, llm)
                    
                    # Lưu vào session
                    st.session_state.retriever = retriever
                    st.session_state.rag_pipeline = pipeline
                    st.session_state.document_processed = True
                    st.session_state.current_doc_info = {
                        "filename": uploaded_file.name,
                        "chunks": len(chunks),
                        "size_mb": file_size / (1024*1024)
                    }
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Hoàn thành!")
                    
                    # Cleanup
                    os.unlink(tmp_path)
                    
                    st.success(f"🎉 Đã xử lý thành công! Tạo được {len(chunks)} chunks từ tài liệu.")
                    st.balloons()
                    
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Lỗi khi xử lý tài liệu: {str(e)}")
                    logger.error(f"Document processing error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card metrics-card fade-in">', unsafe_allow_html=True)
    st.markdown("## 📊 Thống kê hệ thống")
    
    if st.session_state.document_processed:
        current_metrics = metrics.get_metrics()
        doc_info = st.session_state.current_doc_info
        
        # Metrics display
        metric_cols = st.columns(3)
        
        with metric_cols[0]:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{doc_info.get('chunks', 0)}</div>
                <div class="metric-label">Chunks</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[1]:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{current_metrics.get('questions_asked', 0)}</div>
                <div class="metric-label">Câu hỏi</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[2]:
            avg_time = current_metrics.get('average_response_time', 0)
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{avg_time:.1f}s</div>
                <div class="metric-label">Thời gian TB</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Response time chart
        if current_metrics.get('response_times'):
            st.markdown("### 📈 Biểu đồ thời gian phản hồi")
            
            response_times = current_metrics['response_times']
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                y=response_times,
                mode='lines+markers',
                name='Thời gian phản hồi',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title="Thời gian phản hồi theo thời gian",
                xaxis_title="Câu hỏi",
                yaxis_title="Thời gian (giây)",
                template="plotly_white",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("📝 Hãy tải lên và xử lý tài liệu để xem thống kê!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chat interface
st.markdown('<div class="card chat-card fade-in">', unsafe_allow_html=True)
st.markdown("## 💬 Trò chuyện với tài liệu")

if st.session_state.rag_pipeline:
    # Chat history display
    chat_container = st.container()
    
    with chat_container:
        for i, exchange in enumerate(st.session_state.chat_history):
            # User message
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🧑 Bạn:</strong><br>
                {exchange['question']}
            </div>
            """, unsafe_allow_html=True)
            
            # Bot message
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 AI:</strong><br>
                {exchange['answer']}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input với form để tránh lỗi session state
    with st.form("chat_form", clear_on_submit=True):
        question = st.text_input(
            "💭 Đặt câu hỏi về tài liệu:",
            placeholder="Ví dụ: Tài liệu này nói về gì?",
            key="chat_input_form"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            ask_button = st.form_submit_button("🚀 Gửi", type="primary")
        
        with col2:
            if st.form_submit_button("🔄 Xóa chat"):
                st.session_state.chat_history = []
                if st.session_state.rag_pipeline:
                    st.session_state.rag_pipeline.clear_memory()
                st.rerun()
    
    # Xử lý câu hỏi từ form
    if question and ask_button:
        with st.spinner("🤔 Đang suy nghĩ..."):
            try:
                if use_streaming:
                    # Streaming response
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    for chunk in st.session_state.rag_pipeline.ask_streaming(question, use_memory=use_memory):
                        full_response += chunk
                        response_placeholder.markdown(f"""
                        <div class="chat-message bot-message">
                            <strong>🤖 AI:</strong><br>
                            {full_response}
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.05)  # Smooth streaming effect
                    
                    answer = full_response
                else:
                    # Regular response
                    answer = st.session_state.rag_pipeline.ask(question, use_memory=use_memory)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "timestamp": time.time()
                })
                
                # Rerun để cập nhật UI
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
                logger.error(f"Chat error: {str(e)}")
    
    # Quick questions - sử dụng session state để lưu câu hỏi được chọn
    st.markdown("### 💡 Câu hỏi gợi ý:")
    
    quick_questions = [
        "Tài liệu này nói về chủ đề gì?",
        "Tóm tắt nội dung chính của tài liệu",
        "Có những thông tin quan trọng nào?",
        "Kết luận của tài liệu là gì?"
    ]
    
    # Xử lý quick questions
    for i, q in enumerate(quick_questions):
        if st.button(f"💭 {q}", key=f"quick_{i}"):
            # Lưu câu hỏi vào session state để xử lý
            st.session_state.selected_question = q
            st.rerun()
    
    # Xử lý câu hỏi được chọn từ quick questions
    if "selected_question" in st.session_state and st.session_state.selected_question:
        selected_q = st.session_state.selected_question
        st.session_state.selected_question = None  # Reset
        
        with st.spinner("🤔 Đang suy nghĩ..."):
            try:
                if use_streaming:
                    # Streaming response
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    for chunk in st.session_state.rag_pipeline.ask_streaming(selected_q, use_memory=use_memory):
                        full_response += chunk
                        response_placeholder.markdown(f"""
                        <div class="chat-message bot-message">
                            <strong>🤖 AI:</strong><br>
                            {full_response}
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.05)
                    
                    answer = full_response
                else:
                    answer = st.session_state.rag_pipeline.ask(selected_q, use_memory=use_memory)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": selected_q,
                    "answer": answer,
                    "timestamp": time.time()
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
                logger.error(f"Chat error: {str(e)}")

else:
    st.info("📋 Hãy tải lên và xử lý tài liệu trước khi bắt đầu trò chuyện!")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
    <h3>🚀 RAG Chatbot Pro</h3>
    <p>Powered by LangChain • OpenRouter • Streamlit</p>
    <p>Made with ❤️ by HugeBenevolence</p>
</div>
""", unsafe_allow_html=True)
