# utils/metrics.py

import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class MetricsCollector:
    """Collect and store application metrics"""
    
    def __init__(self, metrics_file: str = "logs/metrics.json"):
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(exist_ok=True)
        self.session_metrics = {
            "start_time": datetime.now().isoformat(),
            "questions_asked": 0,
            "documents_processed": 0,
            "total_chunks": 0,
            "average_response_time": 0.0,
            "response_times": [],
            "errors": 0
        }
    
    def log_question(self, question: str, response_time: float, success: bool = True):
        """Log a question and response time"""
        self.session_metrics["questions_asked"] += 1
        self.session_metrics["response_times"].append(response_time)
        
        if success:
            # Calculate average response time
            times = self.session_metrics["response_times"]
            self.session_metrics["average_response_time"] = sum(times) / len(times)
        else:
            self.session_metrics["errors"] += 1
        
        self._save_metrics()
    
    def log_document_processed(self, filename: str, chunk_count: int):
        """Log document processing"""
        self.session_metrics["documents_processed"] += 1
        self.session_metrics["total_chunks"] += chunk_count
        self._save_metrics()
    
    def _save_metrics(self):
        """Save metrics to file"""
        try:
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_metrics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Metrics save error: {e}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return self.session_metrics.copy()

# Singleton metrics
_metrics_instance = None

def get_metrics() -> MetricsCollector:
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = MetricsCollector()
    return _metrics_instance
