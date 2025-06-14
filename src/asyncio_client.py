import asyncio
import socketio
import re

sio = socketio.AsyncClient()
response_data = None
response_event = asyncio.Event()


@sio.on("model_response")
async def on_model_response(data):
    global response_data
    raw_text = data["message"]["content"].strip()
    html = format_llama_response(raw_text)
    response_data = {"response": html}
    response_event.set()


async def send_prompt_to_model(message: str, student_code: str):
    await sio.connect("http://localhost:8001")
    await sio.emit("send_prompt", {"student_code": student_code, "prompt": message})

    # ✅ Wait until the response is received
    await response_event.wait()
    await sio.disconnect()

    return response_data


def format_llama_response(text: str) -> str:
    # Convert **bold** to <strong>
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    # Match numbered list items
    list_items = re.findall(r"^\d+\.\s+(.*)", text, re.MULTILINE)
    if list_items:
        list_html = "".join(f"<li>{item}</li>" for item in list_items)
        text = re.sub(r"^\d+\.\s+.*", "", text, flags=re.MULTILINE)  # Remove list items from body
        text = f"<ol>{list_html}</ol><br>{text.strip()}"  # Append remaining body

    # Convert remaining newlines to <br>
    text = re.sub(r"\n+", "<br>", text.strip())

    return text
