# config.py

import os
from dataclasses import dataclass
from typing import Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to load Streamlit secrets if available
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        streamlit_secrets = st.secrets
    else:
        streamlit_secrets = None
except ImportError:
    streamlit_secrets = None

def get_env_or_secret(key: str, default: str = "") -> str:
    """Get value from environment variable or Streamlit secrets"""
    # Try environment variable first
    env_value = os.getenv(key)
    if env_value:
        return env_value
    
    # Try Streamlit secrets
    if streamlit_secrets:
        try:
            if key in streamlit_secrets:
                return streamlit_secrets[key]
            # Try nested secrets
            for section in ['api', 'app', 'llm', 'vectorstore', 'cache', 'logging']:
                if section in streamlit_secrets and key in streamlit_secrets[section]:
                    return streamlit_secrets[section][key]
        except Exception:
            pass
    
    return default

@dataclass
class AppConfig:
    """Cấu hình tổng thể cho ứng dụng"""
    # LLM Settings
    openrouter_api_key: str = get_env_or_secret("OPENROUTER_API_KEY", "")
    default_model: str = get_env_or_secret("DEFAULT_MODEL", "mistralai/mistral-7b-instruct")
    temperature: float = float(get_env_or_secret("TEMPERATURE", "0.7"))
    max_tokens: int = int(get_env_or_secret("MAX_TOKENS", "1024"))
    
    # Embedding Settings
    embedding_model: str = get_env_or_secret("EMBEDDING_MODEL", "bkai-foundation-models/vietnamese-bi-encoder")
    
    # Chunking Settings
    chunk_size: int = int(get_env_or_secret("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(get_env_or_secret("CHUNK_OVERLAP", "200"))
    min_chunk_size: int = int(get_env_or_secret("MIN_CHUNK_SIZE", "500"))
    breakpoint_threshold: int = int(get_env_or_secret("BREAKPOINT_THRESHOLD", "95"))
    
    # Vector Store Settings
    vector_store_type: str = get_env_or_secret("VECTOR_STORE_TYPE", "smart")
    collection_name: str = get_env_or_secret("COLLECTION_NAME", "rag_documents")
    
    # App Settings
    app_title: str = get_env_or_secret("APP_TITLE", "📚 RAG Chatbot Pro")
    app_description: str = get_env_or_secret("APP_DESCRIPTION", "Chatbot RAG thông minh với khả năng hỏi đáp tài liệu PDF bằng tiếng Việt")
    max_file_size: int = int(get_env_or_secret("MAX_FILE_SIZE", "52428800"))  # 50MB
    supported_formats: list = None
    
    # Cache Settings
    enable_cache: bool = get_env_or_secret("ENABLE_CACHE", "true").lower() == "true"
    cache_ttl: int = int(get_env_or_secret("CACHE_TTL", "3600"))  # 1 hour
    
    # Logging Settings
    log_level: str = get_env_or_secret("LOG_LEVEL", "INFO")
    log_file: Optional[str] = get_env_or_secret("LOG_FILE", "logs/app.log")
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ["pdf", "txt", "docx"]
        
        if not self.openrouter_api_key:
            raise ValueError("⚠️ OPENROUTER_API_KEY is required in .env file or Streamlit secrets")

# Singleton instance
app_config = AppConfig()
