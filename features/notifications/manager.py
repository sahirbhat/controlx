from fastapi import WebSocket
from typing import List



class ConnectionManger:
    def __init__(self):
        self.active_connections:List[WebSocket] = []


    async def connect(self ,websocket:WebSocket) :
        await websocket.accept()
        self.active_connections.append(websocket) 
        print(f'the number of conections are {self.active_connections}')


    def disconnect(self,websocket:WebSocket) :
        self.active_connections.remove(websocket)
        print(f" Client disconnected. Total: {len(self.active_connections)}")


    async def broadcast(self,msg:str) :
        for connection in self.active_connections:
            await connection.send_text(msg)


manager =  ConnectionManger()
          

       
    


