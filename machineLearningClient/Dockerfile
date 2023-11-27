FROM python:3.10.3-slim-bullseye

WORKDIR /app/machineLearningClient

COPY requirements.txt /app/machineLearningClient/

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        libopenblas-dev \
        liblapack-dev \
        libx11-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/machineLearningClient

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6000

ENV MONGODB_URI="mongodb://mongo:27017/"
ENV MONGODB_DATABASE="database1"

CMD ["python", "recognition.py"]
