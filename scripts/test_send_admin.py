import asyncio

from app.config import settings
from app.whatsapp import send_message


async def test():
    admin = settings.WHATSAPP_ADMIN_ID
    print(f"Sending test to {admin}...")
    await send_message(
        admin, "⚠️ Teste de conexão do CaçaLog.\nSe recebeu isso, o envio está funcionando."
    )


if __name__ == "__main__":
    asyncio.run(test())
