# Importing necessary modules from FastAPI
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Creating an instance of the Jinja2Templates class for HTML templates
templates = Jinja2Templates(directory="template")

# Creating a FastAPI app instance
app = FastAPI()

# Endpoint for rendering the home page
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("/index.html", {"request": request})

# List to store active WebSocket connections
websocket_list = []

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accepting the WebSocket connection
    await websocket.accept()

    # Adding the WebSocket to the list if not already present
    if websocket not in websocket_list:
        websocket_list.append(websocket)

    # Continuously listening for incoming messages
    while True:
        data = await websocket.receive_text()
        
        # Broadcasting the received message to all connected WebSockets
        for web in websocket_list:
            if web != websocket:
                await web.send_text(f"{data}")
