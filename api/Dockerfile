FROM python:3.8

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:sumo/stable
RUN apt-get install -y sumo sumo-tools sumo-doc

RUN pip install fastapi uvicorn

ENV SUMO_HOME /usr/share/sumo

WORKDIR /app
COPY ./ /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
