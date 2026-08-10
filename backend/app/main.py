import socketio
from fastapi import FastAPI
from app.tracker import measure_latency
from app.database import init_db, log_latency

# initialize socket.io
socket_init = socketio.AsyncServer(async_mode="asgi", cross_origin_origins="*")

# initialize FastAPI app
fastapi_app = FastAPI(title="PingPal API")

@fastapi_app.on_event("startup")
async def startup():
    await init_db()

@fastapi_app.get("/api/scan")
async def test_scan():
    latency, status = await measure_latency()
    await log_latency(latency, status)
    return {"latency": latency, "status": status}

@fastapi_app.get("/health")
async def health_check():
    return {"status": "online", "message": "PingPal API is running!"}

@fastapi_app.get("/api/ping")
async def test_ping():
    latency, status = await measure_latency()
    return {"latency": latency, "status": status}

# combine socket.io and FastAPI into a single ASGI application
app = socketio.ASGIApp(socket_init, fastapi_app)