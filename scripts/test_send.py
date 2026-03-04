import sys
import os
import asyncio
# Setup path
sys.path.append(os.getcwd())

from app.whatsapp import send_message
from app.config import settings

async def main():
    # Send to the Admin ID (User himself)
    target = settings.WHATSAPP_ADMIN_ID
    print(f"Sending test message to {target}...")
    
    # We need to run this in an async loop
    await send_message(target, "🤖 Testando envio de mensagem via API. Se você receber isso, a API está funcionando.")

if __name__ == "__main__":
    asyncio.run(main())
