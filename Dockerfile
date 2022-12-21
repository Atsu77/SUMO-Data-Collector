FROM python:3.8

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:sumo/stable
RUN apt-get install -y sumo sumo-tools sumo-doc

RUN pip install fastapi uvicorn

ENV SUMO_HOME /usr/share/sumo

COPY static/ /app/static
COPY api/ /app/api

WORKDIR /app

EXPOSE 8000
ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
