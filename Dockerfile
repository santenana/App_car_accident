FROM python:3.10

RUN apt-get update && apt-get install -y \
    python3-opencv \
    gnome-screenshot \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["caraccident", "run", "caraccident_app.py", "--server.port=8501", "--server.address=0.0.0.0"]