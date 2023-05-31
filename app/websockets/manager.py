from fastapi import WebSocket
import asyncio


class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.connections:
            try:
                await connection.send_text(message)
            except RuntimeError:
                self.disconnect(connection)


manager = ConnectionManager()