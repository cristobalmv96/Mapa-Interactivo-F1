FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pandas plotly dash

EXPOSE 8050

CMD ["python", "mapa.py"]
