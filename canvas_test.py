import httpx
import random
import asyncio

# Endpoint URL
URL = "http://localhost:8000/pixel"

# Canvas boyutu
CANVAS_SIZE = 150

# Renk listesi
colors = [
    "#6d001a",
    "#be0039",
    "#ff4500",
    "#ffa800",
    "#ffd635",
    "#fff8b8",
    "#00a368",
    "#00cc78",
    "#7eed56",
    "#00756f",
    "#009eaa",
    "#00ccc0",
    "#2450a4",
    "#3690ea",
    "#51e9f4",
    "#493ac1",
    "#6a5cff",
    "#94b3ff",
    "#811e9f",
    "#b44ac0",
    "#e4abff",
    "#de107f",
    "#ff3881",
    "#ff99aa",
    "#6d482f",
    "#9c6926",
    "#ffb470",
    "#000000",
    "#515252",
    "#898d90",
    "#d4d7d9",
    "#ffffff",
]

async def send_random_pixel(client: httpx.AsyncClient):
    x = random.randint(0, CANVAS_SIZE - 1)
    y = random.randint(0, CANVAS_SIZE - 1)
    color = random.choice(colors)

    payload = {
        "x": x,
        "y": y,
        "color": color
    }

    try:
        response = await client.post(URL, json=payload)
        if response.status_code == 200:
            print(f"Gönderildi: x={x}, y={y}, color={color}")
        else:
            print(f"HATA: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

async def main():
    async with httpx.AsyncClient() as client:
        while True:
            await send_random_pixel(client)
            await asyncio.sleep(0.2)  # 0.5 saniyede bir gönderim

asyncio.run(main())
