from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List, Optional
import hashlib
import os

from config import app_config
from utils.logger import get_logger
from utils.cache import get_cache
from utils.metrics import get_metrics


class PDFProcessor:
    def __init__(self, embedding_model=None):
        """
        Khởi tạo PDFProcessor với mô hình embedding.
        Nếu không truyền vào, dùng mô hình tiếng Việt từ BKAI.
        """
        self.logger = get_logger()
        self.cache = get_cache()
        self.metrics = get_metrics()
        
        self.logger.info("Khởi tạo PDFProcessor...")
        
        self.embedding_model = embedding_model or HuggingFaceEmbeddings(
            model_name=app_config.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        self.semantic_splitter = SemanticChunker(
            embeddings=self.embedding_model,
            buffer_size=1,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=app_config.breakpoint_threshold,
            min_chunk_size=app_config.min_chunk_size,
            add_start_index=True
        )
        
        self.logger.success("PDFProcessor đã khởi tạo thành công")

    def load_and_chunk(self, file_path: str) -> List[Document]:
        """
        Đọc file PDF và chia thành các đoạn (chunk) ngữ nghĩa.
        Trả về danh sách chunks với caching.
        """
        try:
            # Tạo cache key từ file path và modification time
            file_stat = os.stat(file_path)
            cache_key = f"pdf_chunks_{hashlib.md5(file_path.encode()).hexdigest()}_{file_stat.st_mtime}"
            
            # Kiểm tra cache
            if app_config.enable_cache:
                cached_chunks = self.cache.get(cache_key)
                if cached_chunks:
                    self.logger.info(f"Sử dụng cache cho file: {os.path.basename(file_path)}")
                    return cached_chunks
            
            self.logger.info(f"Đang xử lý file: {os.path.basename(file_path)}")
            
            # Load PDF
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            if not documents:
                raise ValueError("Không thể đọc được nội dung từ file PDF")
            
            self.logger.info(f"Đã tải {len(documents)} trang từ PDF")
            
            # Chunk documents
            chunks = self.semantic_splitter.split_documents(documents)
            
            # Cache kết quả
            if app_config.enable_cache:
                self.cache.set(cache_key, chunks)
            
            # Log metrics
            self.metrics.log_document_processed(os.path.basename(file_path), len(chunks))
            
            self.logger.success(f"Đã chia thành {len(chunks)} chunks semantic")
            return chunks
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xử lý PDF: {str(e)}")
            raise
    
    def get_document_info(self, file_path: str) -> dict:
        """Lấy thông tin cơ bản về document"""
        try:
            file_stat = os.stat(file_path)
            return {
                "filename": os.path.basename(file_path),
                "size": file_stat.st_size,
                "size_mb": round(file_stat.st_size / (1024 * 1024), 2),
                "modified": file_stat.st_mtime
            }
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy thông tin file: {str(e)}")
            return {}
