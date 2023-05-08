from datetime import timedelta
from time import time

from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

# from app.database.database import engine, SessionLocal, DataBase
from app.database.database import DataBase
from app.dependencies import get_db, get_settings, get_session_local, get_sql_alchemy_engine
from app.routers import users, news
from app.websockets import chat


settings = get_settings()

app = FastAPI(title="УИТИиА", version="1.0",
              dependencies=[Depends(get_db)])

origins = [
    "http://localhost",
    "http://localhost:8000",
    settings.client_url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(users.router)
app.include_router(news.router)
app.include_router(chat.router)
# app.add_api_websocket_route("/chat", chat.websocket_chat)


class JWTSettings(BaseModel):
    authjwt_secret_key: str = settings.authjwt_secret_key
    authjwt_access_token_expires: int = timedelta(minutes=5)
    authjwt_refresh_token_expires: int = timedelta(weeks=4)
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return JWTSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         # request.state.db = SessionLocal()
#         request.state.db = get_session_local()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response


@app.on_event("startup")
def startup(db: Session = Depends(get_db)):
    start = time()
    connected = False
    while not connected:
        try:
            # DataBase.metadata.create_all(bind=engine)
            DataBase.metadata.create_all(bind=get_sql_alchemy_engine())
            connected = True
        except OperationalError as e:
            if time() - start > settings.timeout:
                raise e


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/chat/");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)
