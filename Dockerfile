FROM python:alpine3.9
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN apt install -y libjpeg-dev zlib1g-dev
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install matplotlib
RUN pip install -r requirements.txt
CMD ["python", "main.py"]