from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict], stream: bool = False, max_tokens: int | None = None) -> str:
        ...
