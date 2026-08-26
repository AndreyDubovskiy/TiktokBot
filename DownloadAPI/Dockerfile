FROM python:3.9-slim
WORKDIR /app
RUN mkdir /app/DownloadAPI
COPY . /app/DownloadAPI
RUN pip install --upgrade pip
RUN pip install playwright
RUN playwright install
RUN pip install -r DownloadAPI/requirements.txt
CMD ["python", "DownloadAPI/main.py"]