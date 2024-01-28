FROM python:alpine3.9
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN apk add --no-cache tesseract-ocr python3 py3-numpy && \
    pip3 install --upgrade pip setuptools wheel && \
    apk add --no-cache --virtual .build-deps gcc g++ zlib-dev make python3-dev py-numpy-dev jpeg-dev && \
    pip3 install matplotlib && \
    apk del .build-deps
RUN pip install -r requirements.txt
RUN apk add --no-cache ffmpeg
CMD ["python", "main.py"]