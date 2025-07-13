import httpx
from app.settings import settings

async def get_sentiment_analyse(complaint_str: str) -> str:
    try:
        async with httpx.AsyncClient(headers={"apikey": settings.api_layer_key}) as client:
            resp = await client.post(
                url='https://api.apilayer.com/sentiment/analysis',
                data=complaint_str
            )

        return resp.json().get('sentiment') or 'unknown'

    except Exception as e:
        return 'unknown'