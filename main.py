import uvicorn

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from backend.api import router as api_router

from backend.app.config import config
from infrastructure.database.setup import create_engine, create_session_pool


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.run_api.api_host,
        port=config.run_api.api_port,
        reload=True,
    )
