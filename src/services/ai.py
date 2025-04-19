import json
from typing import AsyncGenerator, List

import aiohttp

from src.core.config import settings
from src.models.models import Message, Ticket


class AIService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.api_url = f"{settings.GROQ_API_URL}/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _format_messages(self, ticket: Ticket, messages: List[Message]) -> str:
        formatted_messages = []
        for msg in messages:
            role = "Assistant" if msg.is_ai else "Customer"
            formatted_messages.append(f"{role}: {msg.content}")
        return "\n".join(formatted_messages)

    def _create_prompt(self, ticket: Ticket, messages: List[Message]) -> str:
        message_history = self._format_messages(ticket, messages)
        return f"""You are a helpful customer support assistant. 
The customer has the following issue: {ticket.description}

Previous messages:
{message_history}

Provide a helpful response that addresses their concern:"""

    async def generate_response(
        self, ticket: Ticket, messages: List[Message]
    ) -> AsyncGenerator[str, None]:
        prompt = self._create_prompt(ticket, messages)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": "mixtral-8x7b-32768",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                },
            ) as response:
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line.decode("utf-8").strip("data: "))
                            if content := data.get("choices", [{}])[0].get("delta", {}).get("content"):
                                yield content
                        except json.JSONDecodeError:
                            continue


ai_service = AIService() 