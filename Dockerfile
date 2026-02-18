FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Install system deps for pillow and PyTorch (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev ca-certificates wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "-w", "1"]
