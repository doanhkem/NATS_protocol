FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1
RUN mkdir /etc/NATS/
WORKDIR /etc/NATS/
RUN apk add build-base && \
  apk add git && \
  git clone https://github.com/doanhkem/NATS_protocol.git /etc/NATS/ && \
  pip install -r requirements.txt && \
  apk del build-base linux-headers pcre-dev openssl-dev && \
  rm -rf /var/cache/apk/*
CMD ["python", "NATS.py"]