import json
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api import router as api_router
from backend.app.config import config
from backend.app.dependencies import get_repo
from backend.core.services.websocket import (
    GlobalChatWebsocket,
    PrivateChatWebsocket,
    WebsocketService,
)
from infrastructure.database.repo.requests import RequestsRepo

app = FastAPI()

app.mount("/media/", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = WebsocketService()


@app.websocket("/ws/global/{user_id}")
async def websocket_global_chat(
    websocket: WebSocket,
    user_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    global_chat_handler = GlobalChatWebsocket(manager, repo=repo)
    await global_chat_handler.handle_connection(websocket, user_id)


@app.websocket("/ws/private/{user_id}/{recipient_id}")
async def websocket_private_chat(
    websocket: WebSocket,
    user_id: int,
    recipient_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    private_chat_handler = PrivateChatWebsocket(manager, repo=repo)
    await private_chat_handler.handle_connection(websocket, user_id, recipient_id)


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.run_api.api_host,
        port=config.run_api.api_port,
        reload=True,
    )
