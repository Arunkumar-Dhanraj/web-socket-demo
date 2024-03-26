from fastapi import FastAPI, WebSocket, Request, Response, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4

# Creating an instance of the Jinja2Templates class for HTML templates
templates = Jinja2Templates(directory="template")

# Creating a FastAPI app instance
app = FastAPI()

# Dictionary to store WebSocket connections with session IDs
websocket_sessions = {}

# List to store messages
messages = []

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: str = Cookie(None)):
    try:
        # Accepting the WebSocket connection
        await websocket.accept()
        print("WebSocket connection established")
        
        # Add WebSocket connection to the dictionary with session ID
        if session_id in websocket_sessions:
            websocket_sessions[session_id].add(websocket)
        else:
            websocket_sessions[session_id] = {websocket}
        
        # Sending previous messages to the client
        for msg in messages:
            await websocket.send_text(msg)
        
        # Continuously listening for incoming messages
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            
            # Broadcasting the received message to all connected WebSockets in the session
            for web in websocket_sessions.get(session_id, []):
                if web != websocket:
                    await web.send_text(data)
            
            # Storing message in the list
            messages.append(data)
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        # Cleanup on WebSocket closure
        print("WebSocket connection closed")
        if session_id in websocket_sessions:
            websocket_sessions[session_id].remove(websocket)

# Endpoint to fetch previous messages
@app.get("/messages")
async def get_messages():
    return JSONResponse(content=messages)

# Endpoint for rendering the home page
@app.get("/")
async def home(request: Request, response: Response):
    # Generate a session ID if not present in the cookies
    session_id = request.cookies.get("session_id", str(uuid4()))
    response.set_cookie("session_id", session_id)
    return templates.TemplateResponse("/index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6006)
