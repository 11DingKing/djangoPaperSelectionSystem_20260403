# 论文选题系统 - Django后端 Dockerfile

FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 复制项目文件
COPY . .

# 创建目录并设置权限
RUN mkdir -p logs staticfiles && touch logs/app.log && chmod +x entrypoint.sh

# 收集静态文件
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# 暴露端口
EXPOSE 8000

# 启动脚本
ENTRYPOINT ["./entrypoint.sh"]
