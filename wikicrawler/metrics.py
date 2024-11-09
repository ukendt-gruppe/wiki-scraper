from datetime import datetime
import logging
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class CrawlerMetrics:
    start_time: datetime = field(default_factory=datetime.utcnow)
    successful_inserts: int = 0
    failed_inserts: int = 0
    duplicate_urls: int = 0
    processed_urls: List[str] = field(default_factory=list)
    errors: Dict[str, int] = field(default_factory=dict)

    def log_success(self, url: str):
        self.successful_inserts += 1
        self.processed_urls.append(url)

    def log_duplicate(self, url: str):
        self.duplicate_urls += 1
        self.processed_urls.append(url)

    def log_error(self, error_type: str, url: str):
        self.failed_inserts += 1
        self.errors[error_type] = self.errors.get(error_type, 0) + 1
        
    def get_summary(self) -> dict:
        duration = (datetime.utcnow() - self.start_time).total_seconds()
        return {
            "duration_seconds": duration,
            "successful_inserts": self.successful_inserts,
            "failed_inserts": self.failed_inserts,
            "duplicate_urls": self.duplicate_urls,
            "total_processed": len(self.processed_urls),
            "errors_by_type": self.errors
        } 