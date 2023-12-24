import os, sys
import traceback

import openai
from typing import Dict, Any


DEFAULT_GPT_MODEL: str = "gpt-3.5-turbo"

class ChatGPTTesterJa():

    def __init__(self, test_config: Dict[str, Any], test_config_dir: str):

        openai_key: str = os.environ.get('OPENAI_KEY', os.environ.get('OPENAI_API_KEY', ""))
        if not openai_key:
            print("environment variable OPENAI_KEY is not defined.")
            sys.exit(1)
        self._openai_client = openai.OpenAI(api_key=openai_key)
        openai.api_key = openai_key
        self._gpt_model: str = test_config.get("model", DEFAULT_GPT_MODEL)
        self._context: str = ""
        self._generation_instruction: str = ""
        self._temperature = 0.7
        self._user_name = test_config.get("user_name")
        if not self._user_name:
            print("The name of simulated user is not specified in the config.")
            sys.exit(1)

    def set_parameters(self, situation: str, generation_instruction: str, temperature: float) -> None:
        """
        setting simulator parameters
        :param situation: situation string
        :param generation_instruction: request to generate next utterance
        :param temperature: temperature for GPT
        :return: None
        """

        self._context = situation
        self._generation_instruction = generation_instruction
        self._temperature = temperature

    def get_gpt_model(self):

        return self._gpt_model

    def get_next_user_utterance(self, system_utterance: str):

        self._context += f"AI 「{system_utterance}」"

        prompt = self._context + self._generation_instruction

        response = None


        chat_completion = None
        while True:
            try:
                chat_completion = self._openai_client.with_options(timeout=10).chat.completions.create(
                    model=self._gpt_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    )
            except openai.APITimeoutError:
                continue
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                if not chat_completion:
                    continue
                else:
                    break
        user_utterance: str = chat_completion.choices[0].message.content
        user_utterance = user_utterance.replace(self._user_name, "").replace("「", "").replace("」", "")
        self._context += f"{self._user_name} 「{user_utterance}」"

        return user_utterance

