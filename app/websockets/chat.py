from datetime import datetime
import json

from fastapi import WebSocket, WebSocketException, WebSocketDisconnect, Depends, Query
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repositories import users


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # async def send_personal_message(self, message: dict, websocket: WebSocket):
    #     await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


MESSAGE_TYPES = {
    'MESSAGE': 'message',
    'CONNECTION': 'connection',
    'DISCONNECTION': 'disconnection'
}


async def websocket_chat(websocket: WebSocket, token: str = Query(...), session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    await manager.connect(websocket)
    try:
        Authorize.jwt_optional("websocket",token=token)
        raw = Authorize.get_raw_jwt(token)
        if raw:
            curr_user = users.get_user_by_id(int(raw['sub']), session)
            if not curr_user:
                raise WebSocketException(status_code=400, detail=[{'msg': 'User does not exist'}])
        else:
            curr_user = None
        
        await manager.broadcast(json.dumps({'type': MESSAGE_TYPES['CONNECTION'], 'email': curr_user.email, 'datatime': datetime.utcnow()}, default=str))

        while True:
            data = await websocket.receive_text()
            await manager.broadcast(json.dumps({'type': MESSAGE_TYPES['MESSAGE'], 'text': data, 'email': curr_user.email, 'datatime': datetime.utcnow()}, default=str))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({'type': MESSAGE_TYPES['DISCONNECTION'], 'email': curr_user.email, 'datatime': datetime.utcnow()}, default=str))

    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()



# async def websocket_chat(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client left the chat")