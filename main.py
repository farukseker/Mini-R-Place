from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
from fastapi.middleware.cors import CORSMiddleware


# host.docker.internal
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için uygundur, prod'da kısıtla
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host="host.docker.internal", port=2000, db=0, decode_responses=True)

CANVAS_SIZE = 150  # 50x50'lik bir canvas

class Pixel(BaseModel):
    x: int
    y: int
    color: str  # örn: "#FF0000"

def pixel_key(x, y):
    return f"pixel:{x}:{y}"

from fastapi import WebSocket, WebSocketDisconnect

active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Ping-pong için, gerekirse
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_pixel(x, y, color):
    for connection in active_connections:
        await connection.send_json({"x": x, "y": y, "color": color})

@app.get("/canvas")
def get_canvas():
    canvas = []
    for y in range(CANVAS_SIZE):
        row = []
        for x in range(CANVAS_SIZE):
            color = r.get(pixel_key(x, y)) or "#FFFFFF"
            row.append(color)
        canvas.append(row)
    return {"canvas": canvas}

from fastapi import BackgroundTasks

@app.post("/pixel")
async def set_pixel(pixel: Pixel, background_tasks: BackgroundTasks):
    # ... mevcut kod ...
    r.set(pixel_key(pixel.x, pixel.y), pixel.color)
    background_tasks.add_task(broadcast_pixel, pixel.x, pixel.y, pixel.color)
    return {"status": "ok"}

@app.get("/pixel/{x}/{y}")
def get_pixel(x: int, y: int):
    if not (0 <= x < CANVAS_SIZE and 0 <= y < CANVAS_SIZE):
        raise HTTPException(status_code=400, detail="Geçersiz koordinat")
    color = r.get(pixel_key(x, y)) or "#FFFFFF"
    return {"x": x, "y": y, "color": color}