FROM python:3.8.5-slim-buster

ENV TZ=Asia/Shanghai

# 设置软件源（删除注释行，替换 url）
RUN sed -i -e '/^#/d' -e 's|://[^/]*|://mirrors.aliyun.com|' /etc/apt/sources.list

WORKDIR /app

COPY etc/aioserver-example.json /etc/aioserver.json

COPY requirements.txt .

# 不使用缓存，采用阿里云 pypi
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

ADD . .

CMD ["python", "-m", "aioserver.cli"]
