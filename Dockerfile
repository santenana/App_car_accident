FROM python:3.10


WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6006

CMD ["streamlit", "run", "caraccident_app.py", "--server.port=6006", "--server.address=0.0.0.0"]