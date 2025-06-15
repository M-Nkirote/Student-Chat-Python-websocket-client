import asyncio
import socketio
import re

sio = socketio.AsyncClient()
response_data = None
response_event = asyncio.Event()


@sio.event
async def connect():
    print("Connected to server")


@sio.event
async def disconnect():
    print("Disconnected from server")


@sio.on("model_response")
async def on_model_response(data):
    global response_data
    raw_text = data.get("response", "").strip()  # Adjust key if server response differs
    html = format_llama_response(raw_text)
    response_data = html
    response_event.set()


async def connect_to_server():
    if not sio.connected:
        await sio.connect("http://localhost:8001")


async def disconnect_from_server():
    if sio.connected:
        await sio.disconnect()


async def send_prompt_to_model(message: str, student_code: str):
    # Make sure connection is alive before sending prompt
    await connect_to_server()

    response_event.clear()
    await sio.emit("send_prompt", {"student_code": student_code, "prompt": message})
    await response_event.wait()
    return response_data


def format_llama_response(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    list_items = re.findall(r"^\d+\.\s+(.*)", text, re.MULTILINE)
    if list_items:
        list_html = "".join(f"<li>{item}</li>" for item in list_items)
        text = re.sub(r"^\d+\.\s+.*", "", text, flags=re.MULTILINE)
        text = f"<ol>{list_html}</ol><br>{text.strip()}"
    text = re.sub(r"\n+", "<br>", text.strip())
    return text
