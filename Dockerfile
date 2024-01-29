FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir matplotlib pandas
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install ffmpeg-python
CMD ["python", "main.py"]