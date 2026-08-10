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
socket_init = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


def enrich_devices(raw_devices: list[dict], known_devices: dict[str, dict]) -> list[dict]:
    """Merge raw ARP scan results with database records so every device
    carries its name, first_seen, and last_seen."""
    enriched = []
    for dev in raw_devices:
        mac = dev["mac"]
        known = known_devices.get(mac, {})
        enriched.append({
            "mac": mac,
            "ip": dev["ip"],
            "name": known.get("name", ""),
            "first_seen": known.get("first_seen"),
            "last_seen": known.get("last_seen"),
        })
    return enriched


@socket_init.on("connect")
async def on_connect(sid: str, environ: dict):
    """Push the current device list as soon as a client connects."""
    raw = await scan_network()
    known = await get_known_devices()
    devices = enrich_devices(raw, known)
    await socket_init.emit("device_list_update", {"devices": devices}, to=sid)


async def background_monitoring():
    """Continuously monitor the network for new devices and latency."""
    while True:
        try:
            latency, status = await measure_latency()
            await log_latency(latency, status)
            await socket_init.emit("latency_update", {"latency": latency, "status": status})

            # Scan for new devices
            raw_devices = await scan_network()
            known_devices = await get_known_devices()

            for dev in raw_devices:
                mac = dev["mac"]
                ip = dev["ip"]

                # check for new devices
                if mac not in known_devices:
                    await save_device(mac, ip)
                    await send_alert("New Device Detected", f"MAC: {mac}, IP: {ip}")
                    await socket_init.emit("new_device", {"mac": mac, "ip": ip})
                else:
                    await save_device(mac, ip, name=known_devices[mac]["name"])

            # stream current active devices — enriched with db data
            enriched = enrich_devices(raw_devices, known_devices)
            await socket_init.emit("device_list_update", {"devices": enriched})

        except Exception as e:
            print(f"Error in background monitoring: {e}")

        await asyncio.sleep(settings.PING_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    tasks = asyncio.create_task(background_monitoring())
    yield
    tasks.cancel()


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


@fastapi_app.get("/api/devices")
async def get_devices():
    """REST endpoint to pull the current device list."""
    raw = await scan_network()
    known = await get_known_devices()
    return {"devices": enrich_devices(raw, known)}


# combine socket.io and FastAPI into a single ASGI application
app = socketio.ASGIApp(socket_init, fastapi_app)
