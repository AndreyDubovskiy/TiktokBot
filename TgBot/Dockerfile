FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir matplotlib pandas
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install ffmpeg-python
RUN pip install playwright
RUN playwright install
RUN mkdir -p /app/tmp_stat
RUN mkdir -p /app/post_tmp
CMD ["python", "main.py"]