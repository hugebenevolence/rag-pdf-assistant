# modules/llm_wrapper.py

import os
from typing import Optional, Dict, Any
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import app_config
from utils.logger import get_logger


class LLMWrapper:
    def __init__(self, model_name: Optional[str] = None):
        """
        Khởi tạo LLMWrapper với model từ OpenRouter.
        """
        self.logger = get_logger()
        self.model_name = model_name or app_config.default_model
        
        self.logger.info(f"Khởi tạo LLM: {self.model_name}")
        
        if not app_config.openrouter_api_key:
            raise ValueError("⚠️ Không tìm thấy OPENROUTER_API_KEY trong file .env")

        self.llm = ChatOpenAI(
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=app_config.openrouter_api_key,
            model=self.model_name,
            temperature=app_config.temperature,
            max_tokens=app_config.max_tokens,
            streaming=True  # Enable streaming for better UX
        )
        
        self.logger.success("LLM đã khởi tạo thành công")

    def get_llm(self):
        """Trả về LLM instance"""
        return self.llm
    
    def create_vietnamese_system_prompt(self) -> str:
        """Tạo system prompt được tối ưu cho tiếng Việt"""
        return """Bạn là một trợ lý AI thông minh và hữu ích, chuyên trả lời câu hỏi dựa trên nội dung tài liệu được cung cấp.

Hướng dẫn trả lời:
1. Chỉ trả lời dựa trên thông tin có trong tài liệu được cung cấp
2. Nếu không tìm thấy thông tin liên quan, hãy nói "Tôi không tìm thấy thông tin này trong tài liệu"
3. Trả lời bằng tiếng Việt một cách tự nhiên và dễ hiểu
4. Cung cấp câu trả lời chi tiết và có cấu trúc rõ ràng
5. Nếu có thể, hãy trích dẫn phần liên quan từ tài liệu
6. Luôn lịch sự và chuyên nghiệp

Hãy trả lời câu hỏi của người dùng dựa trên ngữ cảnh được cung cấp."""
    
    def test_connection(self) -> Dict[str, Any]:
        """Test kết nối LLM"""
        try:
            response = self.llm.invoke([
                HumanMessage(content="Xin chào, bạn có thể trả lời bằng tiếng Việt không?")
            ])
            
            return {
                "status": "success",
                "model": self.model_name,
                "response": response.content[:100] + "..." if len(response.content) > 100 else response.content
            }
        except Exception as e:
            self.logger.error(f"Lỗi khi test LLM: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
