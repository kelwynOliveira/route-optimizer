FROM python:3.12-slim
WORKDIR /app
COPY app/ /app/
COPY .env /app/.env

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ coinor-cbc \
    && rm -rf /var/lib/apt/lists/*
    
# Virtual environment
RUN python3 -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Packages installation
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "main.py"]