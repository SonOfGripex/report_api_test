import httpx

async def get_ip_info(ip: str):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://ip-api.com/json/{ip}")

        return resp.json().get('country') or None

    except Exception:
        return