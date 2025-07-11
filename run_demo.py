# run_demo.py

"""
Demo script để test RAG Chatbot Pro
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.pdf_processor import PDFProcessor
from modules.vector_store import VectorStore
from modules.llm_wrapper import LLMWrapper
from modules.rag_pipeline import RAGPipeline
from utils.logger import get_logger
from utils.metrics import get_metrics
from config import app_config

def main():
    """Demo chính"""
    logger = get_logger()
    metrics = get_metrics()
    
    logger.info("🚀 Bắt đầu demo RAG Chatbot Pro")
    
    # Đường dẫn tới file PDF demo
    pdf_path = ""
    
    if not os.path.exists(pdf_path):
        logger.error(f"Không tìm thấy file PDF: {pdf_path}")
        return
    
    try:
        # 1. Xử lý PDF
        logger.info("📚 Đang xử lý tài liệu PDF...")
        processor = PDFProcessor()
        chunks = processor.load_and_chunk(pdf_path)
        logger.success(f"Đã tạo {len(chunks)} chunks từ tài liệu")
        
        # 2. Tạo vector store
        logger.info("🔍 Đang xây dựng vector store...")
        vector_store = VectorStore(processor.embedding_model)
        retriever = vector_store.build_store(chunks)
        logger.success("Vector store đã sẵn sàng")
        
        # 3. Khởi tạo LLM
        logger.info("🤖 Đang khởi tạo LLM...")
        llm = LLMWrapper().get_llm()
        logger.success("LLM đã sẵn sàng")
        
        # 4. Tạo RAG pipeline
        logger.info("🔗 Đang tạo RAG pipeline...")
        pipeline = RAGPipeline(retriever, llm)
        logger.success("RAG pipeline đã sẵn sàng")
        
        # 5. Demo questions
        demo_questions = [
            "Tài liệu này nói về chủ đề gì?",
            "Mục tiêu của dự án là gì?",
            "Có những yêu cầu kỹ thuật nào?",
            "Cần làm gì để hoàn thành dự án?",
            "Tóm tắt những điểm quan trọng nhất"
        ]
        
        print("\n" + "="*80)
        print("🎯 DEMO RAG CHATBOT PRO")
        print("="*80)
        
        for i, question in enumerate(demo_questions, 1):
            print(f"\n🔸 Câu hỏi {i}: {question}")
            print("-" * 60)
            
            # Trả lời với streaming
            print("🤖 Trả lời: ", end="", flush=True)
            for chunk in pipeline.ask_streaming(question, use_memory=True):
                print(chunk, end="", flush=True)
            print("\n")
            
            # Nhấn Enter để tiếp tục
            if i < len(demo_questions):
                input("Nhấn Enter để tiếp tục...")
        
        # 6. Hiển thị metrics
        print("\n" + "="*80)
        print("📊 METRICS & STATISTICS")
        print("="*80)
        
        current_metrics = metrics.get_metrics()
        pipeline_info = pipeline.get_pipeline_info()
        
        print(f"📈 Tổng số câu hỏi: {current_metrics['questions_asked']}")
        print(f"📄 Tài liệu đã xử lý: {current_metrics['documents_processed']}")
        print(f"🧩 Tổng số chunks: {current_metrics['total_chunks']}")
        print(f"⏱️ Thời gian phản hồi trung bình: {current_metrics['average_response_time']:.2f}s")
        print(f"❌ Số lỗi: {current_metrics['errors']}")
        print(f"🧠 Memory size: {pipeline_info['memory_size']}")
        print(f"🔧 Retriever type: {pipeline_info['retriever_type']}")
        
        # 7. Chat tương tác
        print("\n" + "="*80)
        print("💬 CHAT TƯƠNG TÁC")
        print("="*80)
        print("Nhập câu hỏi (hoặc 'quit' để thoát):")
        
        while True:
            try:
                user_input = input("\n🧑 Bạn: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                print("🤖 AI: ", end="", flush=True)
                for chunk in pipeline.ask_streaming(user_input, use_memory=True):
                    print(chunk, end="", flush=True)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Tạm biệt!")
                break
        
        # 8. Xuất báo cáo
        print("\n" + "="*80)
        print("📊 XUẤT BÁO CÁO")
        print("="*80)
        
        final_metrics = metrics.get_metrics()
        conversation_history = pipeline.get_conversation_history()
        
        report = {
            "session_summary": {
                "questions_asked": final_metrics['questions_asked'],
                "documents_processed": final_metrics['documents_processed'],
                "total_chunks": final_metrics['total_chunks'],
                "average_response_time": final_metrics['average_response_time'],
                "errors": final_metrics['errors']
            },
            "conversation_history": conversation_history,
            "pipeline_info": pipeline_info
        }
        
        # Lưu báo cáo
        import json
        from datetime import datetime
        
        report_filename = f"demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Báo cáo đã được lưu vào: {report_filename}")
        
        logger.success("🎉 Demo hoàn thành!")
        
    except Exception as e:
        logger.error(f"❌ Lỗi trong demo: {str(e)}")
        raise

if __name__ == "__main__":
    main()
