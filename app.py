# app.py

import streamlit as st
import tempfile
from modules.pdf_processor import PDFProcessor
from modules.vector_store import VectorStore
from modules.llm_wrapper import LLMWrapper
from modules.rag_pipeline import RAGPipeline


st.set_page_config(page_title="📚 RAG Chatbot", layout="wide")
st.title("📚 RAG Chatbot hỏi đáp tài liệu PDF bằng tiếng Việt")

st.markdown("1. **Tải file PDF**  →  2. **Đặt câu hỏi**  →  3. **Nhận câu trả lời** ��")

# Session states
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

# 1. Upload PDF
uploaded_file = st.file_uploader("📤 Tải lên file PDF", type="pdf")

if uploaded_file:
    if st.button("⚙️ Xử lý tài liệu"):
        with st.spinner("⏳ Đang xử lý..."):
            # Lưu file tạm
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Load model & pipeline
            processor = PDFProcessor()
            chunks = processor.load_and_chunk(tmp_path)

            vector = VectorStore(processor.embedding_model)
            retriever = vector.build_store(chunks)

            llm = LLMWrapper().get_llm()

            pipeline = RAGPipeline(retriever, llm)

            # Lưu vào session
            st.session_state.retriever = retriever
            st.session_state.rag_pipeline = pipeline

        st.success("✅ Đã xử lý xong tài liệu!")

# 2. Hỏi đáp
if st.session_state.rag_pipeline:
    question = st.text_input("💬 Đặt câu hỏi:")
    if question:
        with st.spinner("🤖 Đang tạo câu trả lời..."):
            answer = st.session_state.rag_pipeline.ask(question)
        st.write("### 📥 Câu trả lời:")
        st.success(answer)
