FROM python:3.9-slim
WORKDIR /app
RUN mkdir /app/SendingAPI
COPY . /app/SendingAPI
RUN pip install --upgrade pip
RUN pip install -r SendingAPI/requirements.txt
CMD ["python", "SendingAPI/main.py"]