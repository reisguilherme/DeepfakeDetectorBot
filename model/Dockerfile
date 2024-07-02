FROM python:3.9-slim

WORKDIR /app

COPY ./model/ /app/model/

RUN pip install --no-cache-dir -r /app/model/requirements.txt

EXPOSE 6969

CMD ["python", "/app/model/inference/endpoint.py"]
