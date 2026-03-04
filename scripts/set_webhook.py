import sys
import os
import httpx
import asyncio

# Setup path
sys.path.append(os.getcwd())
from app.config import settings

async def main():
    base_url = "http://localhost:8080"
    instance = settings.EVOLUTION_INSTANCE
    token = settings.EVOLUTION_TOKEN

    webhook_url = "http://host.docker.internal:8000/webhook"
    
    headers = {
        "apikey": token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "webhook": {
            "url": webhook_url,
            "enabled": True,
            "events": [
                "MESSAGES_UPSERT"
            ]
        }
    }
    
    print(f"Setting webhook for instance '{instance}' to '{webhook_url}'...")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/webhook/set/{instance}",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Webhook set successfully!")
            print(response.json())
        else:
            print(f"❌ Failed to set webhook. Status: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
