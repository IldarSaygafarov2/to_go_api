import json


FIELDS = [
    "gasoline",
    "ai-80",
    "ai-91",
    "ai-92",
    "ai-95",
    "ai-98",
    "diesel",
    "wc",
    "wifi",
    "shop",
    "parking",
    "car_wash",
    "tire_service",
    "gas",
    "methane",
    "propane",
    "praying_room",
    "electric_charging",
    "cafe",
]


def _convert_empty_values(json_object: dict):
    json_object_copy = json_object.copy()
    for key, value in json_object_copy.items():
        if key in FIELDS:
            print(json_object[key])
            if value == "":
                json_object[key] = False
    return json_object


def _collect_data(json_list: list):
    return [_convert_empty_values(obj) for obj in json_list]


def get_test_places(path: str):
    with open(path, "r", encoding="utf-8") as file:
        content = json.load(file)

    return _collect_data(content)


from pprint import pprint

# pprint(get_test_places("external/data/places.json"))
