FROM python:latest

ENV PYTHONPATH=/app

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000", "--debug"]
