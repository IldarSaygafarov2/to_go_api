import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api import router as api_router
from backend.app.config import config

app = FastAPI()

app.mount("/media/", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_users = {}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket.accept()

    # Store the WebSocket connection in the dictionary
    connected_users[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()

            # Send the received data to the other user
            for user, user_ws in connected_users.items():
                if user == user_id:
                    await user_ws.send_text(data)
    except:
        # If a user disconnects, remove them from the dictionary
        del connected_users[user_id]
        await websocket.close()


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.run_api.api_host,
        port=config.run_api.api_port,
        reload=True,
    )
