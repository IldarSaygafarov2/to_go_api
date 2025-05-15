from typing import Annotated

from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import Depends, FastAPI, Form, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from admin.main import admin_router
from backend.api import router as api_router
from backend.app.config import config
from backend.app.dependencies import get_repo
from backend.core.services.auth import UnauthenticatedUser, AuthUser
from backend.core.services.websocket import (
    GlobalChatWebsocket,
    PrivateChatWebsocket,
    WebsocketService,
    SupportChatWebsocket,
)
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.setup import create_engine, create_session_pool
from backend.core.interfaces.gmail import GmailMessageSchema
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# from send_email import send_email_background, send_email_async


async def connect_to_session():
    engine = create_engine(config.db)
    _session = create_session_pool(engine)
    async with _session() as session:
        repo = RequestsRepo(session)
    return repo


app = FastAPI()

app.mount("/media/", StaticFiles(directory="media"), name="media")
app.mount("/static/", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_home_page(request: Request):
    print(request)
    return templates.TemplateResponse(
        request, "website/index.html", {"request": request}
    )


conf = ConnectionConfig(
    MAIL_USERNAME=config.gmail.mail_username,
    MAIL_PASSWORD=config.gmail.mail_password,
    MAIL_FROM=config.gmail.mail_from,
    MAIL_PORT=config.gmail.mail_port,
    MAIL_SERVER=config.gmail.mail_server,
    MAIL_FROM_NAME=config.gmail.mail_from_name,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


@app.post("/send_email")
async def send_form_email(
    request: Request, form_data: Annotated[GmailMessageSchema, Form()]
):
    message = MessageSchema(
        subject=form_data.subject,
        recipients=[config.gmail.mail_from],
        body=form_data.message,
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return templates.TemplateResponse(
        request, "website/index.html", {"request": request, "is_sent": True}
    )


@app.middleware("http")
async def session_middleware(request: Request, call_next):
    cookie_val = request.cookies.get("session")
    if cookie_val:
        request.scope["session"] = cookie_val
    else:
        request.scope["session"] = config.session.session_choices

    response = await call_next(request)
    response.set_cookie(
        "session",
        value=request.session,
        max_age=config.session.max_age,
        httponly=True,
    )
    return response


@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    token = request.cookies.get("session")
    repo = await connect_to_session()
    if not token:
        request.scope["auth"] = ["anonymous"]
        request.scope["user"] = UnauthenticatedUser()
    else:
        session = await repo.auth_session.get_session_by_token(token=token)
        if session is None:
            request.scope["auth"] = ["anonymous"]
            request.scope["user"] = UnauthenticatedUser()
        else:
            auth_user = AuthUser(session, repo)
            request.scope["user"] = auth_user
            user = await auth_user.user()
            request.scope["_user"] = user
            request.scope["auth"] = user.scope
    response = await call_next(request)
    return response


manager = WebsocketService()


@app.websocket("/ws/global/{user_id}")
async def websocket_global_chat(
    websocket: WebSocket,
    user_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    print("AAAAAAA")
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


@app.websocket("/ws/support/{user_id}/{operator_id}")
async def websocket_support_chat(
    websocket: WebSocket,
    user_id: int,
    operator_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    support_chat_handler = SupportChatWebsocket(manager, repo=repo)
    await support_chat_handler.handle_connection(websocket, user_id, operator_id)


app.include_router(api_router)
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.run_api.api_host,
        port=config.run_api.api_port,
        reload=True,
    )
