FROM python:3.13-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt /app/

# 安装 UV
RUN pip install --no-cache-dir uv

# 使用 UV 安装依赖
RUN uv pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . /app/

# 暴露端口
EXPOSE 8080

# 启动服务
CMD ["uv", "run", "defillama.py"]