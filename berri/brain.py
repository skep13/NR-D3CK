"""Berri's brain sends chat to the model on the Beelink and keeps history."""

import re

import requests
from requests.exceptions import RequestException

import config
THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL)

class Brain:
    def __init__(self) -> None: 
        self.system_prompt: str = config.PROMPT_PATH.read_text()  # pyright: ignore[reportUnknownMemberType]
        self.history: list[dist[str, str]] = []
        print("[NR brain] prompt ready")

    def ask(self, text: str) -> str | None:
        """send one message (visitor speech or [tag]) and return Berri's reply.

        Returns none if beelink cant be reached"""

        self.history.append({"role": "user", "content": text})

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)

        payload = {
            "model": config.MODEL,
            "messages": messages,
            "max_tokens": config.MAX_TOKENS,
            "temperature": 0.8,
            "chat_template_kwargs": {"enable_thinking": False},
        }
        headers = {"Authorisation": f"Bearer {config.API_KEY}"}

        try:
            response = requests.post(
                config.BRAIN_URL,
                json=payload,
                headers=headers,
                timeout=config.TIMEOUT,
            )
            response.raise_for_status()
            reply: str = response.json()["choices"][0]["message"]["content"]
            except (requests.RequestException, KeyError, IndexError, ValueError) as error:
                print(f"[NR brain] error: {error}")
                self.history.pop() #forget message if failed
                return None

            reply = THINK_BLOCK.sub("", reply).strip()

            self.history.append({"role": "assistant", "content":})