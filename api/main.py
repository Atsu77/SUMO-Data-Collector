import os
import subprocess

from fastapi import FastAPI, Response

from api.models.generation_simuration_config import SumoNetGenerator
from api.models.generation_simuration_config import SumoRowGenerator
from api.models.generation_simuration_config import SumocfgGenerator


app = FastAPI()

@app.get("/")
def root_page():
    return {"message": "Hello World"}

@app.get("/net/create")
def create_net_file(number_of_lanes, road_length):
    try:
        SumoNetGenerator(number_of_lanes, road_length).generate_net_file()
        return {"message": "Net file created"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}


@app.get("/row/create")
def create_row_file(maxSpeed, vehcle_per_hour, begin, end):
    try:
        SumoRowGenerator(maxSpeed, vehcle_per_hour, begin, end).generate_rou_file()
        return {"message": "Row file created"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}

@app.get("/sumocfg/create")
def create_row_file(net_file, rou_file, begin, end, step_length):
    try:
        SumocfgGenerator(net_file, rou_file, begin, end, step_length).generate_conf_file()
        return {"message": "Sumocfg file created"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}


@app.get("/simulation/start")
def simulation_start():
    try:
        os.system("sumo -c simulation/sumocfg")
        return {"message": "Simulation start"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}


