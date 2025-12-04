# 1. 基础镜像
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# 2. 设置工作目录
WORKDIR /app

# 3. 【关键修改】直接在这里安装依赖，不读文件了，防止出错
# 使用清华源加速下载，确保在国内能装上
RUN pip install --no-cache-dir playwright==1.40.0 requests -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 复制代码
COPY . .

# 5. 设置时区
ENV TZ=Asia/Shanghai

# 6. 启动
CMD ["python", "-u", "core.py"]