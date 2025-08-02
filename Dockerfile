FROM python:3.9-slim
WORKDIR /app
COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/backend .
EXPOSE 5000
CMD ["python", "app.py"]