# config.py

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AppConfig:
    """Cấu hình tổng thể cho ứng dụng"""
    # LLM Settings
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    default_model: str = "mistralai/mistral-7b-instruct"
    temperature: float = 0.7
    max_tokens: int = 1024
    
    # Embedding Settings
    embedding_model: str = "bkai-foundation-models/vietnamese-bi-encoder"
    
    # Chunking Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    min_chunk_size: int = 500
    breakpoint_threshold: int = 95
    
    # Vector Store Settings
    vector_store_type: str = "chroma"
    collection_name: str = "rag_documents"
    
    # App Settings
    app_title: str = "📚 RAG Chatbot Pro"
    app_description: str = "Chatbot RAG thông minh với khả năng hỏi đáp tài liệu PDF bằng tiếng Việt"
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    supported_formats: list = None
    
    # Cache Settings
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour
    
    # Logging Settings
    log_level: str = "INFO"
    log_file: Optional[str] = "app.log"
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ["pdf", "txt", "docx"]
        
        if not self.openrouter_api_key:
            raise ValueError("⚠️ OPENROUTER_API_KEY is required in .env file")

# Singleton instance
app_config = AppConfig()
