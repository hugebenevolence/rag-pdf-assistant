# modules/rag_pipeline.py

import time
from typing import List, Dict, Any, Optional, Iterator
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from config import app_config
from utils.logger import get_logger
from utils.metrics import get_metrics


class ConversationMemory:
    """Quản lý memory của cuộc trò chuyện"""
    
    def __init__(self, max_history: int = 5):
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []
    
    def add_exchange(self, question: str, answer: str):
        """Thêm một cặp hỏi-đáp vào memory"""
        self.history.append({
            "question": question,
            "answer": answer,
            "timestamp": time.time()
        })
        
        # Giữ chỉ max_history exchanges
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self) -> str:
        """Lấy context từ lịch sử cuộc trò chuyện"""
        if not self.history:
            return ""
        
        context_parts = []
        for exchange in self.history[-3:]:  # Lấy 3 exchanges gần nhất
            context_parts.append(f"Câu hỏi: {exchange['question']}")
            context_parts.append(f"Trả lời: {exchange['answer']}")
        
        return "\n".join(context_parts)
    
    def clear(self):
        """Xóa lịch sử cuộc trò chuyện"""
        self.history = []


class RAGPipeline:
    def __init__(self, retriever, llm):
        """
        Kết nối retriever + LLM thành một pipeline hoàn chỉnh.
        """
        self.retriever = retriever
        self.llm = llm
        self.logger = get_logger()
        self.metrics = get_metrics()
        self.memory = ConversationMemory()
        
        self.logger.info("Khởi tạo RAG Pipeline...")
        
        # Tạo custom prompt template cho tiếng Việt
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._create_system_prompt()),
            ("human", "{question}")
        ])
        
        self.logger.success("RAG Pipeline đã khởi tạo thành công")

    def _create_system_prompt(self) -> str:
        """Tạo system prompt tối ưu cho tiếng Việt"""
        return """Bạn là một trợ lý AI thông minh, chuyên trả lời câu hỏi dựa trên nội dung tài liệu được cung cấp.

Ngữ cảnh từ tài liệu:
{context}

Lịch sử cuộc trò chuyện (nếu có):
{chat_history}

Hướng dẫn trả lời:
1. Chỉ trả lời dựa trên thông tin có trong tài liệu được cung cấp
2. Nếu không tìm thấy thông tin liên quan, hãy nói "Tôi không tìm thấy thông tin này trong tài liệu"
3. Trả lời bằng tiếng Việt một cách tự nhiên và dễ hiểu
4. Cung cấp câu trả lời chi tiết và có cấu trúc rõ ràng
5. Nếu có thể, hãy trích dẫn phần liên quan từ tài liệu
6. Luôn lịch sự và chuyên nghiệp
7. Tham khảo lịch sử cuộc trò chuyện để trả lời phù hợp với ngữ cảnh

Hãy trả lời câu hỏi sau:"""

    def _format_docs(self, docs) -> str:
        """Format documents thành text"""
        if not docs:
            return "Không có tài liệu liên quan được tìm thấy."
        
        formatted_docs = []
        for i, doc in enumerate(docs):
            # Thêm metadata nếu có
            source_info = ""
            if hasattr(doc, 'metadata') and doc.metadata:
                page = doc.metadata.get('page', 'N/A')
                source_info = f" (Trang {page})"
            
            formatted_docs.append(f"Tài liệu {i+1}{source_info}:\n{doc.page_content}")
        
        return "\n\n".join(formatted_docs)

    def ask(self, question: str, use_memory: bool = True) -> str:
        """
        Gửi câu hỏi qua pipeline và trả về câu trả lời.
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Đang xử lý câu hỏi: {question[:100]}...")
            
            # Lấy documents liên quan
            docs = self.retriever.invoke(question)
            context = self._format_docs(docs)
            
            # Lấy chat history nếu sử dụng memory
            chat_history = self.memory.get_context() if use_memory else ""
            
            # Tạo prompt
            prompt = self.prompt_template.format(
                context=context,
                chat_history=chat_history,
                question=question
            )
            
            # Gọi LLM
            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            # Lưu vào memory
            if use_memory:
                self.memory.add_exchange(question, answer)
            
            # Log metrics
            response_time = time.time() - start_time
            self.metrics.log_question(question, response_time, success=True)
            
            self.logger.success(f"Đã trả lời câu hỏi trong {response_time:.2f}s")
            return answer
            
        except Exception as e:
            response_time = time.time() - start_time
            self.metrics.log_question(question, response_time, success=False)
            self.logger.error(f"Lỗi khi xử lý câu hỏi: {str(e)}")
            return f"Xin lỗi, đã có lỗi xảy ra khi xử lý câu hỏi của bạn: {str(e)}"
    
    def ask_streaming(self, question: str, use_memory: bool = True) -> Iterator[str]:
        """
        Streaming response cho UX tốt hơn
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Đang xử lý câu hỏi (streaming): {question[:100]}...")
            
            # Lấy documents liên quan
            docs = self.retriever.invoke(question)
            context = self._format_docs(docs)
            
            # Lấy chat history nếu sử dụng memory
            chat_history = self.memory.get_context() if use_memory else ""
            
            # Tạo prompt
            prompt = self.prompt_template.format(
                context=context,
                chat_history=chat_history,
                question=question
            )
            
            # Stream response
            full_response = ""
            for chunk in self.llm.stream(prompt):
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    full_response += content
                    yield content
            
            # Lưu vào memory
            if use_memory:
                self.memory.add_exchange(question, full_response)
            
            # Log metrics
            response_time = time.time() - start_time
            self.metrics.log_question(question, response_time, success=True)
            
            self.logger.success(f"Đã trả lời câu hỏi (streaming) trong {response_time:.2f}s")
            
        except Exception as e:
            response_time = time.time() - start_time
            self.metrics.log_question(question, response_time, success=False)
            self.logger.error(f"Lỗi khi xử lý câu hỏi (streaming): {str(e)}")
            yield f"Xin lỗi, đã có lỗi xảy ra khi xử lý câu hỏi của bạn: {str(e)}"
    
    def clear_memory(self):
        """Xóa memory cuộc trò chuyện"""
        self.memory.clear()
        self.logger.info("Đã xóa lịch sử cuộc trò chuyện")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Lấy lịch sử cuộc trò chuyện"""
        return self.memory.history.copy()
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """Lấy thông tin về pipeline"""
        return {
            "memory_size": len(self.memory.history),
            "max_history": self.memory.max_history,
            "retriever_type": type(self.retriever).__name__,
            "llm_model": getattr(self.llm, 'model_name', 'unknown')
        }
