import os, sys
import openai
from typing import Dict, Any

GENERAL_SITUATION = "アオイとAIが対話をしています。"
REQUEST_GENERATION = "この次に続くアオイの短い発話を生成してください。"
DEFAULT_GPT_MODEL: str = "gpt-3.5-turbo"

class ChatGPTTesterJa():

    def __init__(self, test_config: Dict[str, Any], test_config_dir: str):

        openai_key: str = os.environ.get('OPENAI_KEY', "")
        if not openai_key:
            print("environment variable OPENAI_KEY is not defined.")
            sys.exit(1)
        openai.api_key = openai_key
        self._gpt_model = test_config.get("gpt_model", DEFAULT_GPT_MODEL)

    def initialize(self, situation: str):

        self._context = f" {GENERAL_SITUATION} {situation} "

    def get_next_user_utterance(self, system_utterance: str):

        self._context += f"AI 「{system_utterance}」"

        prompt = self._context + REQUEST_GENERATION

        response = openai.ChatCompletion.create(
            model=self._gpt_model,
            messages=[{"role": "user", "content": prompt}]
        )

        user_utterance = response.choices[0]['message']['content']
        user_utterance = user_utterance.replace("アオイ", "").replace("「", "").replace("」", "")

        self._context += f"アオイ 「{user_utterance}」"

        return user_utterance

