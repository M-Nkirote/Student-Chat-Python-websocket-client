from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from asyncio_client import send_prompt_to_model
from jwt import PyJWTError, ExpiredSignatureError
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../static"))
TEMPLATES_DIR = os.path.abspath(os.path.join(BASE_DIR, "../templates"))

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

SECRET_KEY = "80e15219b79f3a97a240b9b52bdc7910a1493c11f555d2c6106fb23fe0f9ef76dc39355733ad55e79830035fe02296128e2fb4381c6b175169a299da467e6229fcaf0faf8d2c64a118d869106d57c40e36c951908b639a9a6c0d6752ce3c8741f2052b76e7e45dcf8d4454d950c723283cbfa2e4494617a55d72884519e40a9f40ac821bdecfd586a05219cca08fabc2919388ffc42b2a2aa95e5b0d4995a9599c38eadfdb786941e56154d0769aec71c6e0de40ff85e4875a1fc833be5b7d005136edff4775c15e7df590b57691f8f6444000175e332ca405e322855b104ae74fa949f56f3b7c856cb3a36ceeb2d517dc26a85c0d14e73aa2c097b365e4dbaf"
ALGORITHM = "HS256"


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, token: str = Form(...)):
    user_info = decode_token(token)
    if not user_info:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url=f"/chat?token={token}", status_code=status.HTTP_302_FOUND)


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, token: str):
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
    token = body.get("token")
    message = body.get("message")

    user_info = decode_token(token)
    if not user_info:
        return JSONResponse(content={"error": "Invalid token"}, status_code=400)

    response = await send_prompt_to_model(message, user_info["student_code"], user_info["first_name"])
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



