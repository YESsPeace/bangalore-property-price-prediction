from fastapi import FastAPI, HTTPException
import json

from starlette.middleware.cors import CORSMiddleware

from util import get_estimated_price
from pydantic import BaseModel

app = FastAPI()


class PredictionInput(BaseModel):
    location: str
    sqft: float
    bhk: int
    bath: int


# Разрешаем запросы из всех источников (*)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/get_location_names')
def get_location_names():
    with open('../model/columns.json', "r") as file:
        response = {
            'locations': json.load(file)['data_columns'][3:]
        }

        return response


@app.post('/predict_home_price')
def predict_home_price(location: str, sqft: float, bhk: int, bath: int):
    try:
        # Весь остальной код
        response = {
            'estimated_price': get_estimated_price(location, sqft, bhk, bath)
        }

        return response

    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
