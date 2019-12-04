FROM python:3.7.5-slim
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
RUN mkdir -pv /var/log/order
CMD ["python", "invoice.py"]
