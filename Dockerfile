FROM python:3.10-slim

WORKDIR /app

# requirements.txt 在根目录，直接复制
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 复制整个 app 文件夹（包含 main.py 和所有子模块）
COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
