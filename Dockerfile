FROM python:3.9.10-slim

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]