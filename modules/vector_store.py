# modules/vector_store.py

from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List, Optional, Dict, Any
import os
import tempfile

from config import app_config
from utils.logger import get_logger
from utils.cache import get_cache


class VectorStore:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_db = None
        self.logger = get_logger()
        self.cache = get_cache()
        
        self.logger.info("Khởi tạo VectorStore...")

    def build_store(self, documents: List[Document], persist_directory: Optional[str] = None):
        """
        Nhận danh sách document chunks, biến thành vector và lưu trong Chroma.
        Trả về retriever để dùng trong truy vấn RAG.
        """
        try:
            self.logger.info(f"Đang xây dựng vector store với {len(documents)} documents...")
            
            # Tạo persistent directory nếu cần
            if persist_directory is None:
                persist_directory = tempfile.mkdtemp(prefix="chroma_db_")
            
            self.vector_db = Chroma.from_documents(
                documents=documents,
                embedding=self.embedding_model,
                persist_directory=persist_directory,
                collection_name=app_config.collection_name
            )
            
            self.logger.success(f"Vector store đã được xây dựng thành công tại: {persist_directory}")
            
            # Tạo retriever với các tham số tối ưu
            retriever = self.vector_db.as_retriever(
                search_type="mmr",  # Maximum Marginal Relevance
                search_kwargs={
                    "k": 5,  # Số lượng documents trả về
                    "fetch_k": 20,  # Số lượng documents để tính MMR
                    "lambda_mult": 0.5  # Diversity vs relevance balance
                }
            )
            
            return retriever
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xây dựng vector store: {str(e)}")
            raise
    
    def get_similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Tìm kiếm similarity trực tiếp"""
        if not self.vector_db:
            raise ValueError("Vector store chưa được xây dựng")
        
        try:
            results = self.vector_db.similarity_search(query, k=k)
            self.logger.info(f"Tìm thấy {len(results)} documents liên quan")
            return results
        except Exception as e:
            self.logger.error(f"Lỗi khi tìm kiếm: {str(e)}")
            return []
    
    def get_store_info(self) -> Dict[str, Any]:
        """Lấy thông tin về vector store"""
        if not self.vector_db:
            return {"status": "not_built"}
        
        try:
            collection = self.vector_db.get()
            return {
                "status": "active",
                "document_count": len(collection.get("ids", [])),
                "collection_name": app_config.collection_name
            }
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy thông tin store: {str(e)}")
            return {"status": "error", "error": str(e)}
