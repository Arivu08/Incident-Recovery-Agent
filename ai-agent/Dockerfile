FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# 🔧 Create logs folder to avoid logging crash
RUN mkdir -p logs

CMD ["python", "app.py"]
