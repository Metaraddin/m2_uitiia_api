from datetime import datetime
import json

from fastapi import WebSocket, WebSocketException, WebSocketDisconnect, Depends, Query
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repositories import users
from app.websockets.manager import manager


MESSAGE_TYPES = {
    'MESSAGE': 'message',
    # 'CONNECTION': 'connection',
    # 'DISCONNECTION': 'disconnection'
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
        
        # await manager.broadcast(json.dumps({'type': MESSAGE_TYPES['CONNECTION'], 'email': curr_user.email, 'avatar_uri': curr_user.avatar_uri, 'datatime': datetime.utcnow()}, default=str))

        while True:
            data = await websocket.receive_text()
            await manager.broadcast(json.dumps({'type': MESSAGE_TYPES['MESSAGE'], 'text': data, 'email': curr_user.email, 'avatar_uri': curr_user.avatar_uri, 'datatime': datetime.utcnow()}, default=str))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(json.dumps({'type': MESSAGE_TYPES['DISCONNECTION'], 'email': curr_user.email, 'avatar_uri': curr_user.avatar_uri, 'datatime': datetime.utcnow()}, default=str))
    
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        manager.disconnect(websocket)
        await websocket.close()
