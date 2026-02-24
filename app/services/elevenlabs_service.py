import httpx
from app.config.settings import settings


async def generate_tts_audio(text: str, voice_id: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)

   
    if response.status_code != 200:
        print("ElevenLabs API Error:", response.text)
        # Return dummy audio instead of crashing
        raise Exception("TTS service temporarily unavailable")

    return response.content
