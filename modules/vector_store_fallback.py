# modules/vector_store_fallback.py

"""
Fallback vector store implementation using FAISS for Streamlit Cloud compatibility
"""

from typing import List, Optional, Dict, Any
import numpy as np
import pickle
import tempfile
import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever

from config import app_config
from utils.logger import get_logger


class FallbackVectorStore:
    """Fallback vector store using FAISS when ChromaDB is not available"""
    
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_store = None
        self.logger = get_logger()
        
        self.logger.info("Khởi tạo Fallback VectorStore với FAISS...")

    def build_store(self, documents: List[Document], persist_directory: Optional[str] = None):
        """
        Xây dựng vector store với FAISS
        """
        try:
            self.logger.info(f"Đang xây dựng FAISS vector store với {len(documents)} documents...")
            
            # Tạo FAISS vector store
            self.vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embedding_model
            )
            
            # Save to disk nếu có persist_directory
            if persist_directory:
                os.makedirs(persist_directory, exist_ok=True)
                self.vector_store.save_local(persist_directory)
                self.logger.info(f"FAISS vector store saved to: {persist_directory}")
            
            self.logger.success("FAISS vector store đã được xây dựng thành công")
            
            # Tạo retriever
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            )
            
            return retriever
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xây dựng FAISS vector store: {str(e)}")
            raise
    
    def get_similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Tìm kiếm similarity với FAISS"""
        if not self.vector_store:
            raise ValueError("Vector store chưa được xây dựng")
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            self.logger.info(f"Tìm thấy {len(results)} documents liên quan")
            return results
        except Exception as e:
            self.logger.error(f"Lỗi khi tìm kiếm: {str(e)}")
            return []
    
    def get_store_info(self) -> Dict[str, Any]:
        """Lấy thông tin về vector store"""
        if not self.vector_store:
            return {"status": "not_built", "type": "faiss_fallback"}
        
        return {
            "status": "active",
            "type": "faiss_fallback",
            "index_size": self.vector_store.index.ntotal if hasattr(self.vector_store, 'index') else 0
        }


class SmartVectorStore:
    """Smart vector store that tries ChromaDB first, falls back to FAISS"""
    
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_store = None
        self.logger = get_logger()
        self.using_fallback = False
        
        self.logger.info("Khởi tạo Smart VectorStore...")
    
    def build_store(self, documents: List[Document], persist_directory: Optional[str] = None):
        """
        Thử ChromaDB trước, nếu không được thì dùng FAISS
        """
        try:
            # Thử ChromaDB trước
            self.logger.info("Đang thử ChromaDB...")
            from .vector_store import VectorStore
            
            chroma_store = VectorStore(self.embedding_model)
            retriever = chroma_store.build_store(documents, persist_directory)
            
            self.vector_store = chroma_store
            self.using_fallback = False
            self.logger.success("Sử dụng ChromaDB thành công")
            
            return retriever
            
        except Exception as e:
            self.logger.warning(f"ChromaDB không khả dụng: {str(e)}")
            self.logger.info("Chuyển sang FAISS fallback...")
            
            # Fallback to FAISS
            try:
                fallback_store = FallbackVectorStore(self.embedding_model)
                retriever = fallback_store.build_store(documents, persist_directory)
                
                self.vector_store = fallback_store
                self.using_fallback = True
                self.logger.success("Sử dụng FAISS fallback thành công")
                
                return retriever
                
            except Exception as fallback_error:
                self.logger.error(f"Cả ChromaDB và FAISS đều thất bại: {str(fallback_error)}")
                raise
    
    def get_similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Tìm kiếm similarity"""
        if not self.vector_store:
            raise ValueError("Vector store chưa được xây dựng")
        
        return self.vector_store.get_similarity_search(query, k)
    
    def get_store_info(self) -> Dict[str, Any]:
        """Lấy thông tin về vector store"""
        if not self.vector_store:
            return {"status": "not_built"}
        
        info = self.vector_store.get_store_info()
        info["using_fallback"] = self.using_fallback
        info["store_type"] = "faiss" if self.using_fallback else "chromadb"
        
        return info
