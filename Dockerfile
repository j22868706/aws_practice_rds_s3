FROM python:3-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
EXPOSE 3500
CMD ["python", "app.py"]
