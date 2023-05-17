FROM python:3.10
LABEL authors="zym"

# 设置工作目录
WORKDIR /app

# 把当前目录下所有的文件都拷贝到镜像的 /app 目录下
ADD . /app

# 使用 pip 安装依赖
RUN pip install -r requirements.txt
# 指定对外暴露的端口
EXPOSE 8000

# 设置启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]