FROM python:3.9-alpine
WORKDIR /app
COPY app/ /app/
RUN apk add --no-cache gcc g++ musl-dev
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]