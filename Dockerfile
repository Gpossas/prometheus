FROM python:3.10.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/
COPY . /app/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]