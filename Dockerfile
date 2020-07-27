FROM python:3.7

RUN mkdir -p /opt/services/cad/src
RUN mkdir -p /opt/services/cad/src/logs
RUN touch /opt/services/cad/src/logs/cad.log
WORKDIR /opt/services/cad/src

COPY manage.py /opt/services/cad/src
COPY administration/ /opt/services/cad/src
COPY cad/ /opt/services/cad/src
COPY connexion/ /opt/services/cad/src
COPY default/ /opt/services/cad/src
COPY inscription/ /opt/services/cad/src
COPY users/ /opt/services/cad/src
COPY Dockerfile /opt/services/cad/src
COPY requirements.txt /opt/services/cad/src
COPY compress_logs.sh /opt/services/cad/src

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--chdir", "cad", "--bind", ":8000", "cad.wsgi:application"]
