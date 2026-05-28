from openai import AsyncOpenAI

from app.core.config import settings
from app.llm.base import LLMClient


class DeepSeekClient(LLMClient):
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            timeout=120,
        )
        self.model = settings.LLM_MODEL

    async def chat(self, messages: list[dict], stream: bool = False, max_tokens: int | None = None) -> str:
        kwargs = dict(model=self.model, messages=messages, temperature=0.1, stream=False)
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        response = await self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""
