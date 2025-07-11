# utils/logger.py

import logging
import os
from datetime import datetime
from typing import Optional

class CustomLogger:
    """Custom logger với format đẹp và hỗ trợ Tiếng Việt"""
    
    def __init__(self, name: str, level: str = "INFO", log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Tránh duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Formatter với emoji và thời gian
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler nếu có
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, msg: str):
        self.logger.info(f"ℹ️ {msg}")
    
    def warning(self, msg: str):
        self.logger.warning(f"⚠️ {msg}")
    
    def error(self, msg: str):
        self.logger.error(f"❌ {msg}")
    
    def success(self, msg: str):
        self.logger.info(f"✅ {msg}")
    
    def debug(self, msg: str):
        self.logger.debug(f"🔍 {msg}")

# Singleton logger
def get_logger(name: str = "RAG_Chatbot") -> CustomLogger:
    return CustomLogger(name, level="INFO", log_file="logs/app.log")
