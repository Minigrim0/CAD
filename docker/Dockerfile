FROM python:3.8-slim-buster

WORKDIR /srv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y libpq-dev build-essential netcat

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["gunicorn", "cad.wsgi:application", "--bind", "0.0.0.0:8000"]
