FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 定时运行爬虫（每24小时采集一次）
CMD ["sh", "-c", "while true; do scrapy crawl amap -a keyword=家电维修 -a city=南京; sleep 86400; done"]