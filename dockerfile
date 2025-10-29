FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask flask-cors pymongo gunicorn
ENV PORT=8080
CMD ["gunicorn", "-w", "2", "-b", ":8080", "server:app"]
