FROM python:3.7-alpine

COPY fav.json .

COPY server.py .

COPY tester.py .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python3", "-m", "server.py"]

