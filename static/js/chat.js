const socket = io("http://localhost:8001", { transports: ["websocket"] });

socket.on("connect", () => {
  console.log("Connected to model server");
});

socket.on("model_response", function(data) {
  const chatBox = document.getElementById("chat-box");

  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", "model");
  msgDiv.innerHTML = `
    <img src="https://img.icons8.com/laces/64/F25081/school.png" alt="Model">
    <div class="message-content">
      <strong>Model:</strong><br>${data.response}
    </div>
  `;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
});

document.getElementById("chat-form").addEventListener("submit", function(e) {
  e.preventDefault();
  const input = document.getElementById("message");
  const message = input.value;

  const chatBox = document.getElementById("chat-box");
  const userMsgDiv = document.createElement("div");
  userMsgDiv.classList.add("message", "user");
  userMsgDiv.innerHTML = `
    <img src="https://img.icons8.com/laces/64/F25081/school.png" alt="You">
    <div class="message-content">
      <strong>You:</strong><br>${message}
    </div>
  `;
  chatBox.appendChild(userMsgDiv);

  socket.emit("send_prompt", { student_code: "{{ student_code }}", prompt: message });
  input.value = "";
});

document.getElementById("end-session").addEventListener("click", () => {
  socket.disconnect();
  alert("Session ended. Redirecting to login...");
  window.location.href = "/";
});