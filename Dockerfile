FROM python:3.8.5-slim-buster

ENV TZ=Asia/Shanghai

# 设置软件源（删除注释行，替换 url）
RUN sed -i -e '/^#/d' -e 's|://[^/]*|://mirrors.aliyun.com|' /etc/apt/sources.list

WORKDIR /app

COPY etc/aioserver-example.json /etc/aioserver.json

COPY requirements.txt .

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ADD . .

CMD ["python", "-m", "aioserver.cli"]
