# ${\textsf{\color{#C25A7C}💬 Simple Student Chat Client (Frontend + Python Async Client)}}$ 

A dual-interface client for the real-time Student Chat system — combining a browser-based UI and a Python asyncio WebSocket client to simulate or enable student-like behavior during live sessions.

This project interacts with the FastAPI+Socket.IO backend to send prompts, receive model responses, and log structured chats for learning analysis.

## ${\textsf{\color{#C25A7C}Features}}$ 📋
* Clean, user-friendly chat interface (HTML + JavaScript)
* Alternative headless chat interface via Python asyncio client
* Token-based login and session tracking
* Real-time messaging powered by WebSocket (via Socket.IO)
* Seamless integration with backend logging
* End-session handling with UI redirect

## ${\textsf{\color{#C25A7C}Project Structure}}$ 🗂️

```bash
.
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── asyncio_client.py
│   ├── create_dummy_secret_key.py
│   └── main.py
├── static
│   ├── css
│   │   ├── chat.css
│   │   └── login.css
│   ├── images
│   │   └── pink-girl-icon.png
│   └── js
│       └── chat.js
└── templates
    ├── chat.html
    └── login.html
```

## ${\textsf{\color{#C25A7C}Set Up}}$ 🛠️
### ${\textsf{\color{#FFC0CB}Clone the Repo}}$
> `git clone git@github.com:M-Nkirote/Simple-Text-to-SQL-Solution.git`
>
> `cd Student-Chat-Python-websocket-client` 

### ${\textsf{\color{#FFC0CB}Set up virtual environment}}$
> `python -m venv venv`
> 
> `source venv/bin/activate`

### ${\textsf{\color{#FFC0CB}Install dependencies}}$
> `pip install -r requirements.txt`

### ${\textsf{\color{#FFC0CB}To run main.py}}$
> `cd /Student-Chat-Python-websocket-client/src`
> 
> `uvicorn main:app --reload --port 8000`

Note!
You should ensure that the backend server is already running (Refer to the server project: Student-Chat-Python-websocket-server, to set it up.)

## ${\textsf{\color{#C25A7C}Gallery}}$ 📷
### ${\textsf{\color{#FFC0CB}Login Page}}$
<img width="734" alt="Screenshot 2025-06-28 at 14 26 36" src="https://github.com/user-attachments/assets/4259c940-06a8-4d09-82ed-0a5d547190f9" />


### ${\textsf{\color{#FFC0CB}Chat Page}}$
<img width="734" alt="Screenshot 2025-06-28 at 14 22 27" src="https://github.com/user-attachments/assets/82c82e63-e5db-4206-8783-b1004a0a4a4b" />

## ${\textsf{\color{#C25A7C}To create a JWT token}}$ 🔑
* Go to https://jwt.io/
* Select the option "JWT Encoder"
* Add your payload
  <img width="645" alt="Screenshot 2025-06-28 at 14 33 06" src="https://github.com/user-attachments/assets/44af3292-2781-4cb6-ba04-5d7c5bdfe4bc" />
* Add the secret key for encoding
* * To create the random key, after cloning this project, run the file `src/create_dummy_secret_key.py`, and copy the output.
  * Paste the created key in the section 'Sign JWT: Secret' at https://jwt.io/
    <img width="628" alt="Screenshot 2025-06-28 at 14 37 35" src="https://github.com/user-attachments/assets/23cd1638-83ad-4f3c-86ad-4412acd54152" />
* Copy your generated token ☺️
  <img width="1279" alt="Screenshot 2025-06-28 at 14 39 02" src="https://github.com/user-attachments/assets/1228df27-a8aa-44cb-a060-fba028751cd9" />
 

