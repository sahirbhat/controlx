from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .manager import manager
import json
from datetime import datetime

router = APIRouter(tags=["Notifications"])

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.dumps({
                "user": username,
                "message": data,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({
            "user": "system",
            "message": f"{username} left",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }))