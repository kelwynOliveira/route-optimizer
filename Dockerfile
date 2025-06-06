FROM python:3.12-slim
WORKDIR /app
COPY app/ /app/
COPY .env /app/.env
RUN apt-get update && apt-get install -y gcc g++ coinor-cbc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]