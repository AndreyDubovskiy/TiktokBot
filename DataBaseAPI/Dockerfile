FROM python:3.9-slim
WORKDIR /app
RUN mkdir /app/DataBaseAPI
COPY . /app/DataBaseAPI
RUN pip install --upgrade pip
RUN pip install -r DataBaseAPI/requirements.txt
CMD ["python", "DataBaseAPI/main.py"]