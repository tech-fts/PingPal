import asyncio
from contextlib import asynccontextmanager
import socketio
from fastapi import FastAPI

from app.config import settings
from app.tracker import measure_latency
from app.database import init_db, log_latency, save_device, get_known_devices
from app.scanner import scan_network
from app.notifier import send_alert

# initialize socket.io
socket_init = socketio.AsyncServer(async_mode="asgi", cross_origin_origins="*")

async def background_monitoring():
    """Continuously monitor the network for new devices and latency."""
    while True:
        try:
            latency, status = await measure_latency()
            await log_latency(latency, status)
            await socket_init.emit("latency_update", {"latency": latency, "status": status})

            # Scan for new devices
            devices = await scan_network()
            known_devices = await get_known_devices()

            for dev in devices:
                mac = dev["mac"]
                ip = dev["ip"]

                # check for new devices
                if mac not in known_devices:
                    await save_device(mac, ip)
                    await send_alert("New Device Detected", f"MAC: {mac}, IP: {ip}")
                    await socket_init.emit("new_device", {"mac": mac, "ip": ip})
                else:
                    await save_device(mac, ip, name=known_devices[mac]["name"])  # Update existing device info

            # stream current active devices
            await socket_init.emit("device_list_update", {"devices": devices})

        except Exception as e:
            print(f"Error in background monitoring: {e}")

        await asyncio.sleep(settings.PING_INTERVAL)  # Wait for the configured interval before the next scan

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Initialize the database on startup
    tasks = asyncio.create_task(background_monitoring())
    yield
    tasks.cancel()  # Cancel the background monitoring task on shutdown

# initialize FastAPI app
fastapi_app = FastAPI(title="PingPal API", lifespan=lifespan)

@fastapi_app.get("/api/scan")
async def test_scan():
    devices = await scan_network()
    return {"total_discovered": len(devices), "devices": devices}

@fastapi_app.get("/health")
async def health_check():
    return {"status": "online", "message": "PingPal API is running!"}

@fastapi_app.get("/api/ping")
async def test_ping():
    latency, status = await measure_latency()
    await log_latency(latency, status)
    return {"latency": latency, "status": status}

# combine socket.io and FastAPI into a single ASGI application
app = socketio.ASGIApp(socket_init, fastapi_app)