import requests
import logging

logger = logging.getLogger(__name__)


class BackendPipeline:
    """
    将采集结果推送到后端 API
    """
    def __init__(self, backend_url):
        self.backend_url = backend_url
    
    @classmethod
    def from_crawler(cls, crawler):
        backend_url = crawler.settings.get("BACKEND_URL", "http://backend:8000/api")
        return cls(backend_url)
    
    def process_item(self, item, spider):
        try:
            response = requests.post(
                f"{self.backend_url}/leads/ingest",
                json=dict(item),
                timeout=10
            )
            if response.status_code == 200:
                logger.info(f"成功推送: {item.get('name')}")
            else:
                logger.warning(f"推送失败: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"推送异常: {e}")
        return item