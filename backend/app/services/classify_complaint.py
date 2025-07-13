from app.settings import settings
import openai

openai.api_key = settings.openai_key

SYSTEM_PROMPT = (
    'Определи категорию жалобы: "{text}". Варианты: техническая, оплата, другое. '
    "Ответ только одним словом."
)

async def classify(text: str) -> str:
    try:
        resp = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(text=text)}
            ],
            timeout=15,
        )
        cat = resp.choices[0].message.content.strip().lower()
        if cat not in ("техническая", "оплата"):
            cat = "другое"
        return cat
    except Exception:
        return "другое"
