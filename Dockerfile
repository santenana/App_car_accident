FROM python:3.10


WORKDIR /app


COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
COPY . .

EXPOSE 6006

CMD ["streamlit", "run", "caraccident_app.py", "--server.port=6006", "--server.address=0.0.0.0"]