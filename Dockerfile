FROM Python:3.10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    python3-opencv \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .


RUN pip3 install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8501

CMD ["streamlit", "run", "caraccident_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
