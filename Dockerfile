FROM python:3.7

RUN mkdir -p /opt/services/cad/src
WORKDIR /opt/services/cad/src

COPY . /opt/services/cad/src

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--chdir", "cad", "--bind", ":8000", "cad.wsgi:application"]
