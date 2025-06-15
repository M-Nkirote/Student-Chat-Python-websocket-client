const token = window.TOKEN;

const sio = io("http://localhost:8001", {
    auth: { token }  // Optional: send token for server-side validation (if you implement)
  });

  sio.on("connect", () => {
    console.log("Socket connected with id:", sio.id);
  });

  sio.on("disconnect", () => {
    console.log("Socket disconnected");
  });

  // Example to handle model_response if needed on client side
  sio.on("model_response", (data) => {
    console.log("Model response:", data);
    // Update chat UI accordingly
  });

  // Make sio globally accessible (for disconnect on end-session)
  window.sio = sio;

async function sendToBackend(text) {
  const r = await fetch("/send-message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token, message: text })
  });
  return r.json();
}

const chatBox = document.getElementById("chat-box");

function add(role, html) {
  const div = document.createElement("div");
  div.className = "message " + role;
  div.innerHTML = `
    <img src="https://img.icons8.com/laces/64/F25081/school.png">
    <div class="message-content">${html}</div>`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const box = document.getElementById("message");
  const text = box.value.trim();
  if (!text) return;
  add("user", `<strong>You:</strong><br>${text}`);
  box.value = "";

  const data = await sendToBackend(text);
  add("model", `<strong>Model:</strong><br>${data.response}`);
});

document.getElementById("end-session").onclick = async () => {
  if (sio && sio.connected) {
    await sio.disconnect();  // Explicit disconnect
  }
  location.href = "/";
};