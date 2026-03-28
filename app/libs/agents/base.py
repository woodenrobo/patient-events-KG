import litellm

from app.config.environment import settings

MODEL = "gemini/gemini-2.5-flash"


class BaseAgent:
    def __init__(self) -> None:
        pass

    async def complete(self, prompt: str, message: str) -> str:
        response = await litellm.acompletion(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message},
            ],
            api_key=settings.gemini_api_key.get_secret_value(),
            response_format={"type": "json_object"},
            stream=False,
        )
        if not response or not isinstance(response, litellm.ModelResponse):
            return ""

        return response.choices[0].message.content or ""
