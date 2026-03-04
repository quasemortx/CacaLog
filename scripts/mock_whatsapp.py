import httpx
import asyncio
import uuid
import sys
from datetime import datetime

# Config
WEBHOOK_URL = "http://localhost:8000/webhook"
# Must match .env
REMOTE_JID = "120363000000000000@g.us" 

async def send_mock_message(text: str, sender_name: str = "TestUser", sender_number: str = "5511999999999"):
    payload = {
        "type": "message",
        "data": {
            "key": {
                "remoteJid": REMOTE_JID,
                "fromMe": False,
                "id": str(uuid.uuid4())
            },
            "pushName": sender_name,
            "participant": sender_number,
            "message": {
                "conversation": text
            }
        }
    }
    
    print(f"--> Enviando: '{text}'")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(WEBHOOK_URL, json=payload, timeout=10.0)
            print(f"<-- Resposta Server: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"xx Erro ao enviar: {e}")

async def main():
    if len(sys.argv) > 1:
        # Modo interativo: python mock_whatsapp.py "Texto da mensagem"
        text = " ".join(sys.argv[1:])
        await send_mock_message(text)
    else:
        # Modo bateria de testes
        print("=== Iniciando Simulação de Mensagens do WhatsApp ===")
        
        # 1. Sala OK
        await send_mock_message("S-712 ok tudo certo")
        await asyncio.sleep(1)
        
        # 2. Lab Pendente
        await send_mock_message("L-03 pendente sem ssd")
        await asyncio.sleep(1)
        
        # 3. Dois locais na mesma mensagem
        await send_mock_message("21 e 05 com erro de boot")
        await asyncio.sleep(1)
        
        # 4. Comando
        await send_mock_message("/resumo p1")

if __name__ == "__main__":
    asyncio.run(main())
