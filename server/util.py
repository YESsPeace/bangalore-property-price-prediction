import json
import pickle

import numpy as np

import warnings

warnings.filterwarnings('ignore')

__locations = None
__data_columns = None
__model = None


def get_estimated_price(location: str, sqft: float, bhk: int, bath: int):
    global __locations
    global __data_columns
    global __model

    if __locations is None or __data_columns is None or __model is None:
        load_saved_data()

    try:
        loc_index = __data_columns.index(location.lower())

    except Exception as e:
        print(f"Error finding location index: {e}")
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    print("Debug - loc_index:", loc_index)

    return round(__model.predict([x])[0], 2)


def get_location_names():
    return __locations


def load_saved_data():
    global __data_columns
    global __model
    global __locations

    with open('../model/columns.json', "r") as columns_json_file:
        __data_columns = json.load(columns_json_file)['data_columns']
        __locations = __data_columns[3:]

    with open('../model/home_prices_model.pickle', "rb") as model_file:
        __model = pickle.load(model_file)


if __name__ == '__main__':
    load_saved_data()
    print(get_location_names())
    print(get_estimated_price('location_1st Phase JP Nagar', 1000, 2, 2))
