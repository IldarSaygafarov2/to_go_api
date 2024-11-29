import pandas as pd

# togo_places = pd.read_csv("external/data/togo-places.csv")
# togo_comment = pd.read_csv("external/data/togo-comments.csv")
# togo_fuel_price = pd.read_csv("external/data/togp-fuel-price .csv")

# print(togo_fuel_price.head())
fields = [
    "name",
    "category",
    "address",
    "coordinates",
    "phone­_number",
    "yandex_map_link",
    "gasoline",
    "ai-80",
    "ai-91",
    "ai-95",
    "ai-98",
    "diesel",
    "working_hours",
    "wc",
    "shop",
    "parking",
    "car_wash",
    "tire_service",
    "gas",
    "methane",
    "propane",
    "praying_room",
    "electric_charging",
]


def get_togo_places_from_csv(file_path: str):
    places = pd.read_csv(file_path, usecols=fields)
    print(places.info())


get_togo_places_from_csv("external/data/togo-places.csv")
