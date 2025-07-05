from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from asyncio_client import send_prompt_to_model
from jwt import PyJWTError, ExpiredSignatureError
import jwt
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../static"))
TEMPLATES_DIR = os.path.abspath(os.path.join(BASE_DIR, "../templates"))

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, token: str = Form(...)):
    user_info = decode_token(token)
    if not user_info:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    response = RedirectResponse(url="/chat", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="token", value=token, httponly=True, max_age=3600)  # Secure=True in production
    return response


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    token = request.cookies.get("token")
    user_info = decode_token(token)
    if not user_info:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "token": token,
        "student_code": user_info["student_code"],
        "first_name": user_info["first_name"]
    })


@app.post("/send-message")
async def handle_message(request: Request):
    body = await request.json()
    session_id = str(uuid.uuid4())
    token = body.get("token")
    message = body.get("message")

    user_info = decode_token(token)
    if not user_info:
        return JSONResponse(content={"error": "Invalid token"}, status_code=400)

    response = await send_prompt_to_model(message, user_info["student_code"], user_info["first_name"], session_id)
    return {"response": response}


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        student_code = payload.get("student_code")
        first_name = payload.get("first_name")
        if not student_code or not first_name:
            raise ValueError("Required fields missing in token")
        return {"student_code": student_code, "first_name": first_name}
    except ExpiredSignatureError:
        print("Token expired")
        return None
    except PyJWTError as e:
        print(f"Token decode error: {e}")
        return None



