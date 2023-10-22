FROM python:3.11-alpine
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8011
ENV FLASK_APP=app.py
CMD ["python", "app.py"]