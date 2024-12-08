import random
from pathlib import Path
from fastapi import UploadFile

MEDIA_FOLDER = Path("media")


def create_user_profile_dir(user_id: int):
    _dir = MEDIA_FOLDER / "profiles" / str(user_id)
    _dir.mkdir(exist_ok=True, parents=True)
    return _dir


def create_images_dir(path: str):
    _dir = MEDIA_FOLDER / path
    _dir.mkdir(exist_ok=True, parents=True)
    return _dir


def generate_code():
    return "".join(random.sample([f"{i}" for i in range(10)], 4))
