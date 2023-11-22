from fastapi import FastAPI
import json

from util import get_estimated_price

app = FastAPI()


@app.get('/get_location_names')
def get_location_names():
    with open('../model/columns.json', "r") as file:
        response = json.load(file)
        return response


@app.post('/predict_home_price')
def predict_home_price(location: str, sqft: float, bhk: int, bath: int):

    response = {
        'estimated_price': get_estimated_price(location, sqft, bhk, bath)
    }

    return response
