# run_app.py

"""
Script chạy RAG Chatbot Pro với các tùy chọn khác nhau - Fixed Version
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_requirements():
    """Kiểm tra requirements"""
    required_packages = [
        ("streamlit", "Streamlit web framework"),
        ("langchain", "LangChain framework"),
        ("plotly", "Plotly for charts"),
        ("pandas", "Data manipulation"),
        ("numpy", "Numerical computing"),
        ("openai", "OpenAI client"),
        ("chromadb", "Vector database")
    ]
    
    print("📦 Kiểm tra dependencies...")
    missing = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package} ({description})")
        except ImportError:
            missing.append(package)
            print(f"   ❌ {package} ({description}) - Missing")
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ Tất cả dependencies đã được cài đặt!")
    return True

def check_env():
    """Kiểm tra environment variables"""
    if not os.path.exists('.env'):
        print("❌ File .env không tồn tại")
        print("Chạy: python setup_dev.py")
        return False
    
    # Load .env
    try:
        # Simple .env reader
        env_vars = {}
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
        
        api_key = env_vars.get('OPENROUTER_API_KEY', '')
        if not api_key or api_key == 'your_openrouter_api_key_here':
            print("❌ OPENROUTER_API_KEY chưa được cấu hình")
            print("Cập nhật API key trong file .env")
            return False
        
        print("✅ Environment variables OK")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi load .env: {e}")
        return False

def run_streamlit(app_file="app_pro.py", port=8501, host="0.0.0.0", debug=False):
    """Chạy Streamlit app"""
    print(f"🚀 Chạy {app_file} trên {host}:{port}")
    
    cmd = [
        "streamlit", "run", app_file,
        "--server.port", str(port),
        "--server.address", host,
        "--server.headless", "true" if not debug else "false"
    ]
    
    if debug:
        cmd.extend(["--logger.level", "debug"])
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chạy Streamlit: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Streamlit chưa được cài đặt. Chạy: pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Tạm dừng ứng dụng")

def run_demo():
    """Chạy demo tương tác"""
    print("🎮 Chạy demo tương tác...")
    
    if not os.path.exists("run_demo.py"):
        print("❌ File run_demo.py không tồn tại")
        return False
    
    try:
        subprocess.run([sys.executable, "run_demo.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chạy demo: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Tạm dừng demo")
        return True

def run_tests():
    """Chạy tests cơ bản"""
    print("🧪 Chạy tests...")
    
    try:
        # Test imports
        from modules.pdf_processor import PDFProcessor
        from modules.vector_store import VectorStore
        from modules.llm_wrapper import LLMWrapper
        from modules.rag_pipeline import RAGPipeline
        from config import app_config
        from utils.logger import get_logger
        from utils.cache import get_cache
        from utils.metrics import get_metrics
        
        print("✅ Import tests passed")
        
        # Test components
        logger = get_logger("test")
        cache = get_cache()
        metrics = get_metrics()
        
        # Test cache
        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"
        
        print("✅ Component tests passed")
        print("🎉 Tất cả tests đều pass!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def setup_environment():
    """Setup môi trường phát triển"""
    print("🔧 Setup môi trường phát triển...")
    
    if not os.path.exists("setup_dev.py"):
        print("❌ File setup_dev.py không tồn tại")
        return False
    
    try:
        subprocess.run([sys.executable, "setup_dev.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi setup: {e}")
        return False

def main():
    """Hàm chính"""
    parser = argparse.ArgumentParser(
        description="RAG Chatbot Pro - Enhanced Runner Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_app.py --mode app                 # Chạy ứng dụng Pro
  python run_app.py --mode app --port 8502     # Chạy trên port khác
  python run_app.py --mode basic               # Chạy ứng dụng cơ bản
  python run_app.py --mode demo                # Chạy demo tương tác
  python run_app.py --mode test                # Chạy tests
  python run_app.py --mode setup               # Setup môi trường
  python run_app.py --mode check               # Kiểm tra dependencies
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["app", "basic", "demo", "test", "setup", "check"],
        default="app",
        help="Chế độ chạy (default: app)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port cho Streamlit (default: 8501)"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host cho Streamlit (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Bật debug mode"
    )
    
    args = parser.parse_args()
    
    print("🚀 RAG Chatbot Pro - Enhanced Runner")
    print("=" * 50)
    print(f"📋 Mode: {args.mode}")
    if args.mode in ["app", "basic"]:
        print(f"🌐 URL: http://{args.host}:{args.port}")
    if args.debug:
        print("🔍 Debug mode: ON")
    print("=" * 50)
    
    # Pre-flight checks
    if args.mode in ["app", "basic", "demo", "test"]:
        if not check_requirements():
            sys.exit(1)
    
    if args.mode in ["app", "basic", "demo"]:
        if not check_env():
            sys.exit(1)
    
    # Kiểm tra file tồn tại
    if args.mode == "app" and not os.path.exists("app_pro.py"):
        print("❌ File app_pro.py không tồn tại!")
        sys.exit(1)
    
    if args.mode == "basic" and not os.path.exists("app.py"):
        print("❌ File app.py không tồn tại!")
        sys.exit(1)
    
    # Chạy theo mode
    success = True
    
    if args.mode == "app":
        run_streamlit("app_pro.py", args.port, args.host, args.debug)
    elif args.mode == "basic":
        run_streamlit("app.py", args.port, args.host, args.debug)
    elif args.mode == "demo":
        success = run_demo()
    elif args.mode == "test":
        success = run_tests()
    elif args.mode == "setup":
        success = setup_environment()
    elif args.mode == "check":
        success = check_requirements()
    
    if success:
        print("\n✅ Hoàn thành!")
    else:
        print("\n❌ Có lỗi xảy ra!")
        sys.exit(1)

if __name__ == "__main__":
    main()
