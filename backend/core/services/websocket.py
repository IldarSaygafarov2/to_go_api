import json

from fastapi import WebSocket, WebSocketDisconnect

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.chat import Message


class WebsocketService:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.user_connections = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        print("WEBSOCKET", websocket)
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections.remove(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]

    async def send_personal_message(self, message_json: dict, recipint_id: int):
        websocket: WebSocket = self.user_connections.get(recipint_id)
        print("WEBSOCKET", websocket)
        if websocket:
            await websocket.send_text(json.dumps(message_json, ensure_ascii=False))

    async def broadcast(self, message_json: dict):
        for connection in self.active_connections:
            try:
                data = json.dumps(message_json, ensure_ascii=False)
                if message_json.get("type") == "bytes":
                    data = message_json.get("bytes_data").encode()
                    await connection.send_json(message_json)
                else:
                    await connection.send_text(data)
            except WebSocketDisconnect:
                # Если подключение было закрыто, удаляем его из активных соединений
                self.active_connections.remove(connection)


class GlobalChatWebsocket:
    def __init__(self, manager: WebsocketService, repo: RequestsRepo):
        self.manager = manager
        self.repo = repo

    async def handle_connection(self, websocket: WebSocket, user_id: int):
        await self.manager.connect(websocket, user_id)

        try:
            while True:

                _data = await websocket.receive()
                print(_data)
                # print(user_id)
                # print(_data)
                if "bytes" in _data:
                    data = _data.get("bytes")

                    await self.repo.chat_messages.add_global_message(
                        sender_id=user_id,
                        bytes_data=data,
                    )
                    await self.manager.broadcast(
                        {
                            "sender_id": user_id,
                            "type": "bytes",
                            "bytes_data": str(data),
                        }
                    )
                else:
                    # data = await websocket.receive_json()
                    data = json.loads(_data.get("text"))
                    await self.repo.chat_messages.add_global_message(
                        sender_id=int(data["sender_id"]),
                        content=data["content"],
                    )

                    await self.manager.broadcast(data)

        except WebSocketDisconnect:
            self.manager.disconnect(websocket=websocket, user_id=user_id)


class PrivateChatWebsocket:
    def __init__(self, manager: WebsocketService, repo: RequestsRepo):
        self.manager = manager
        self.repo = repo

    async def handle_connection(
        self,
        websocket: WebSocket,
        user_id: int,
        recipient_id: int,
    ):
        await self.manager.connect(websocket, user_id)

        try:
            while True:
                data = await websocket.receive_json()
                chat = await self.repo.private_chats.create_chat_if_not_exists(
                    sender_id=user_id, recipient_id=recipient_id
                )
                print(data)
                if chat is None:
                    chat = await self.repo.private_chats.get_chat(
                        sender_id=user_id, recipient_id=recipient_id
                    )

                await self.repo.chat_messages.add_private_message(
                    sender_id=user_id, content=data["content"], private_chat_id=chat.id
                )
                await self.manager.send_personal_message(data, recipint_id=user_id)

        except WebSocketDisconnect:
            self.manager.disconnect(websocket=websocket, user_id=user_id)


class SupportChatWebsocket:
    def __init__(self, manager: WebsocketService, repo: RequestsRepo):
        self.manager = manager
        self.repo = repo

    async def handle_connection(
        self,
        websocket: WebSocket,
        user_id: int,
        operator_id: int,
    ):
        await self.manager.connect(websocket=websocket, user_id=user_id)
        print(operator_id)
        try:
            while True:
                data = await websocket.receive_json()
                print(data)
        except WebSocketDisconnect:
            self.manager.disconnect(websocket=websocket, user_id=user_id)
