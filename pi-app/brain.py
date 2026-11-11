import queue
import re
import threading

import requests

import config

THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL)


class Brain:
    def __init__(self):
        self.system_prompt = config.PROMPT_PATH.read_text()
        self.history = []
        self._replies = queue.Queue()
        self._busy = False
        print("[NR brain] prompt ready")

    def ask(self, text):
        self.history.append({"role": "user", "content": text})

        messages = [{"role": "system", "content": self.system_prompt}] + self.history

        payload = {
            "model": config.MODEL,
            "messages": messages,
            "max_tokens": config.MAX_TOKENS,
            "temperature": 0.8,
            "chat_template_kwargs": {"enable_thinking": False},
        }
        headers = {"Authorization": f"Bearer {config.API_KEY}"}

        try:
            response = requests.post(config.BRAIN_URL, json=payload, headers=headers, timeout=config.TIMEOUT)
            reply = response.json()["choices"][0]["message"]["content"]
        except Exception as error:
            print(f"[NR brain] error: {error}")
            self.history.pop()  # forget message if failed
            return None

        reply = THINK_BLOCK.sub("", reply).strip()

        self.history.append({"role": "assistant", "content": reply})
        self.history = self.history[-config.MAX_HISTORY:]

        return reply

    def ask_async(self, text):
        # runs ask() in background so the animation doesnt freeze
        # returns False if berri is still busy with the last message
        if self._busy:
            return False
        self._busy = True

        def worker():
            reply = self.ask(text)
            self._replies.put({"text": text, "reply": reply})
            self._busy = False

        threading.Thread(target=worker, daemon=True).start()
        return True

    def get_reply(self):
        # returns {"text", "reply"} when a reply is ready, otherwise None
        try:
            return self._replies.get_nowait()
        except queue.Empty:
            return None

    def reset(self):
        # forget convo when visitor walks away
        self.history = []


if __name__ == "__main__":
    b = Brain()
    print("berri:", b.ask("[waking up]"))
    print("berri:", b.ask("what did i just say"))
