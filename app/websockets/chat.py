from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketException, Depends, Query
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repositories import users


# router = APIRouter(prefix='/chat', tags=['Chat'])


# @router.websocket('/')
# async def websocket_chat(websocket: WebSocket, session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
#     Authorize.jwt_optional()
#     if Authorize.get_jwt_subject():
#         curr_user = users.get_user_by_id(int(Authorize.get_jwt_subject()), session)
#         if not curr_user:
#             raise HTTPException(status_code=400, detail=[{'msg': 'User does not exist'}])
#     else:
#         curr_user = None
    
#     await websocket.accept()
#     while True:
#         text = await websocket.receive_text()
#         await websocket.send_json({'text': text, 'user': curr_user, 'time': datetime.utcnow()})


# @router.websocket('/')
async def websocket_chat(websocket: WebSocket, token: str = Query(...), session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    try:
        Authorize.jwt_optional("websocket",token=token)
        raw = Authorize.get_raw_jwt(token)
        if raw:
            curr_user = users.get_user_by_id(int(raw['sub']), session)
            if not curr_user:
                raise WebSocketException(status_code=400, detail=[{'msg': 'User does not exist'}])
        else:
            curr_user = None

        while True:
            text = await websocket.receive_text()
            await websocket.send_text(f'text: {text}, user: {curr_user.email}, time: {datetime.utcnow()}')
            # await websocket.send_json({'text': text, 'user': curr_user, 'time': datetime.utcnow()})

    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()


# @router.websocket('/')
# async def websocket_chat(websocket: WebSocket, session: Session = Depends(get_db)): 
#     await websocket.accept()
#     while True:
#         text = await websocket.receive_text()
#         await websocket.send_text(text)

# async def websocket_chat(websocket: WebSocket): 
#     await websocket.accept()
#     while True:
#         text = await websocket.receive_text()
#         await websocket.send_text(text)
