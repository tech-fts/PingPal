import httpx
from app.config import settings

<<<<<<< HEAD
async def send_alert(title:str, message:str):
    """Send a notification webhook if a url is configures in settings."""
=======
async def send_alert(title: str, message: str):
    """Send a notification webhook if a URL is configured in settings."""
>>>>>>> backend
    if not settings.DISCORD_WEBHOOK_URL:
        return

    payload = {
<<<<<<< HEAD
        "embeds":[{
=======
        "embeds": [{
>>>>>>> backend
            "title": title,
            "description": message,
            "color": 16711680 if "New" in title else 65280
        }]
    }

    async with httpx.AsyncClient() as client:
        try:
            await client.post(settings.DISCORD_WEBHOOK_URL, json=payload)
        except httpx.RequestError as e:
<<<<<<< HEAD
            print(f"Failed to send alert: {e}")
=======
            print(f"Failed to send alert: {e}")
>>>>>>> backend
