import litellm
from pydantic import BaseModel

from app.config.environment import settings

MODEL = "gemini/gemini-2.5-flash"


class BaseAgent:
    def __init__(self) -> None:
        pass

    async def complete[T: BaseModel](
        self,
        prompt: str,
        message: str,
        response_model: type[T],
    ) -> T:
        response = await litellm.acompletion(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message},
            ],
            api_key=settings.gemini_api_key.get_secret_value(),
            response_format=response_model,
            stream=False,
        )
        if not isinstance(response, litellm.ModelResponse):
            raise ValueError("Unexpected streaming response")
        content = response.choices[0].message.content or ""
        return response_model.model_validate_json(content)
