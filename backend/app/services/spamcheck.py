import httpx
from app.settings import settings


async def is_spam(text: str) -> bool:
    try:
        if not settings.api_layer_key:
            return False

        async with httpx.AsyncClient(headers={"apikey": settings.api_layer_key}) as client:
            resp = await client.post(
                url="https://api.apilayer.com/spamchecker?threshold=2.5",
                data=text,
            )

        return resp.json().get('is_spam') or False

    except Exception as e:
        return False