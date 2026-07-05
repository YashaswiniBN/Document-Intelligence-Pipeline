import asyncio
import json
import logging
from datetime import datetime
from error_handler import DocumentResult, ProcessingStatus

logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self, pipeline, concurrency: int = 3):
        self.pipeline    = pipeline
        self.semaphore   = asyncio.Semaphore(concurrency)
        self.results     = []
        self.start_time  = None

    async def process_one(self, doc_id: str, text: str) -> dict:
        async with self.semaphore:
            logger.info(f"Processing doc {doc_id}")
            try:
                result = await asyncio.to_thread(
                    self.pipeline.process_document, text
                )
                return {"doc_id": doc_id, **result}
            except Exception as e:
                logger.error(f"Doc {doc_id} failed: {e}")
                return {
                    "doc_id": doc_id,
                    "status": ProcessingStatus.FAILED,
                    "error":  str(e)
                }

    async def run(self, documents: list[dict]) -> dict:
        self.start_time = datetime.now()
        tasks = [
            self.process_one(doc["id"], doc["text"])
            for doc in documents
        ]
        results = await asyncio.gather(*tasks)
        elapsed = (datetime.now() - self.start_time).total_seconds()

        summary = {
            "total":        len(results),
            "success":      sum(1 for r in results if r.get("status") == "success"),
            "needs_review": sum(1 for r in results if r.get("status") == "needs_review"),
            "failed":       sum(1 for r in results if r.get("status") == "failed"),
            "elapsed_sec":  round(elapsed, 2),
            "results":      results
        }
        logger.info(f"Batch done: {summary['success']}/{summary['total']} success in {elapsed:.1f}s")
        return summary