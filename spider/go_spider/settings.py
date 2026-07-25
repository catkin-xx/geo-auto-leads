BOT_NAME = "geo_spider"
SPIDER_MODULES = ["geo_spider.spiders"]
NEWSPIDER_MODULE = "geo_spider.spiders"

# 遵守 robots.txt
ROBOTSTXT_OBEY = False

# 下载延迟（避免被封）
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# 并发设置
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Pipeline
ITEM_PIPELINES = {
    "geo_spider.pipelines.BackendPipeline": 300,
}

# 后端地址
BACKEND_URL = "http://backend:8000/api"

# 日志
LOG_LEVEL = "INFO"