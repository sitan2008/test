FROM python:3.9.10-slim

COPY . .

CMD ["python", "main.py"]