from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect

from rmq import AioRMQ

app = FastAPI(
    title='heyling_test'
)

rabbit = AioRMQ()


@app.post('/queue_reverse_text')
async def reverse_text(text: str):
    if not rabbit.is_ready:
        await rabbit.setup('test')
    await rabbit.push(text)


@app.websocket("/listen_results")
async def websocket_endpoint(websocket: WebSocket):
    await rabbit.connect(websocket)
    try:
        while True:
            await websocket.receive_bytes()
    except WebSocketDisconnect:
        rabbit.remove(websocket)
