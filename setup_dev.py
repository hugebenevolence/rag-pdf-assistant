# setup_dev.py

"""
Script setup môi trường development cho RAG Chatbot Pro
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description=""):
    """Chạy command và hiển thị kết quả"""
    print(f"🔄 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(f"Output: {result.stdout}")
        else:
            print("❌ Error!")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    return True

def create_directories():
    """Tạo các thư mục cần thiết"""
    directories = [
        "logs",
        "cache", 
        "uploads",
        "models",
        "docs",
        "tests",
        "data"
    ]
    
    print("📁 Tạo directories...")
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   ✅ {dir_name}/")

def create_env_file():
    """Tạo file .env mẫu"""
    env_content = """# OpenRouter API Key
OPENROUTER_API_KEY=your_openrouter_api_key_here

# App Configuration
APP_TITLE="RAG Chatbot Pro"
APP_DESCRIPTION="Chatbot RAG thông minh với khả năng hỏi đáp tài liệu PDF bằng tiếng Việt"
MAX_FILE_SIZE=52428800  # 50MB

# LLM Configuration
DEFAULT_MODEL="mistralai/mistral-7b-instruct"
TEMPERATURE=0.7
MAX_TOKENS=1024

# Vector Store Configuration
EMBEDDING_MODEL="bkai-foundation-models/vietnamese-bi-encoder"
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MIN_CHUNK_SIZE=500

# Cache Configuration
ENABLE_CACHE=true
CACHE_TTL=3600

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Đã tạo file .env")
    else:
        print("ℹ️ File .env đã tồn tại")

def install_requirements():
    """Cài đặt requirements"""
    print("📦 Cài đặt Python packages...")
    
    if not run_command("pip install --upgrade pip", "Upgrade pip"):
        return False
    
    if not run_command("pip install -r requirements.txt", "Install requirements"):
        return False
    
    return True

def setup_git():
    """Setup git repository"""
    print("🔧 Setup Git...")
    
    if not os.path.exists('.git'):
        run_command("git init", "Initialize git repository")
        run_command("git add .", "Add all files")
        run_command("git commit -m 'Initial commit'", "Initial commit")
    else:
        print("ℹ️ Git repository đã tồn tại")

def run_tests():
    """Chạy tests cơ bản"""
    print("🧪 Chạy tests...")
    
    # Test import modules
    try:
        from modules.pdf_processor import PDFProcessor
        from modules.vector_store import VectorStore
        from modules.llm_wrapper import LLMWrapper
        from modules.rag_pipeline import RAGPipeline
        from config import app_config
        from utils.logger import get_logger
        from utils.cache import get_cache
        from utils.metrics import get_metrics
        
        print("✅ Tất cả modules import thành công")
        
        # Test logger
        logger = get_logger()
        logger.info("Test logging")
        print("✅ Logger hoạt động")
        
        # Test cache
        cache = get_cache()
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        assert value == "test_value"
        print("✅ Cache hoạt động")
        
        # Test metrics
        metrics = get_metrics()
        current_metrics = metrics.get_metrics()
        assert isinstance(current_metrics, dict)
        print("✅ Metrics hoạt động")
        
        print("🎉 Tất cả tests cơ bản đã pass!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def main():
    """Hàm chính"""
    print("🚀 RAG Chatbot Pro - Development Setup")
    print("="*50)
    
    # Kiểm tra Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version}")
    
    # Setup steps
    steps = [
        ("Tạo directories", create_directories),
        ("Tạo file .env", create_env_file),
        ("Cài đặt requirements", install_requirements),
        ("Setup Git", setup_git),
        ("Chạy tests", run_tests)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        try:
            if not step_func():
                print(f"❌ {step_name} failed!")
                break
        except Exception as e:
            print(f"❌ {step_name} error: {e}")
            break
    else:
        print("\n🎉 Setup hoàn thành!")
        print("\n📖 Bước tiếp theo:")
        print("1. Cập nhật OPENROUTER_API_KEY trong file .env")
        print("2. Chạy: streamlit run app_pro.py")
        print("3. Hoặc chạy demo: python run_demo.py")
        print("\n🔗 Tài liệu: README.md")
        return
    
    print("\n❌ Setup không thành công!")
    print("Vui lòng kiểm tra lại các lỗi phía trên")

if __name__ == "__main__":
    main()
