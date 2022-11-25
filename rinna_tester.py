import torch
from transformers import T5Tokenizer, AutoModelForCausalLM
import os

class RinnaTester():

    def __init__(self):

        self._tokenizer = T5Tokenizer.from_pretrained(os.path.join(os.path.dirname(__file__),
                                                             "models/tokenizer-japanese-gpt-1b"))
        self._model = AutoModelForCausalLM.from_pretrained(os.path.join(os.path.dirname(__file__),
                                                                       "models/model-japanese-gpt-1b"))
        if torch.cuda.is_available():
            self._model = self._model.to("cuda")

        self._context = ""

    def initialize_dialogue(self, situation: str, system_prompt: str) -> str:

        self._context = f"{situation} AI:「{system_prompt}」ユウキ:「"
        next_utterance = self._get_next_utterance(self._context)
        return next_utterance

    def proceed_dialogue(self, system_utterance: str) -> str:

        self._context += system_utterance + "」人間:「"
        next_utterance = self._get_next_utterance(self._context)
        return next_utterance

    def _get_next_utterance(self, context: str):

        token_ids = self._tokenizer.encode(context, add_special_tokens=False, return_tensors="pt")

        with torch.no_grad():
            output_ids = self._model.generate(
                token_ids.to(self._model.device),
                max_length=200,
                min_length=100,
                do_sample=True,
                top_k=500,
                top_p=0.95,
                pad_token_id=self._tokenizer.pad_token_id,
                bos_token_id=self._tokenizer.bos_token_id,
                eos_token_id=self._tokenizer.eos_token_id,
                bad_word_ids=[[self._tokenizer.unk_token_id]]
            )
        output = self._tokenizer.decode(output_ids.tolist()[0])

        self._context = self._context.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        output = output.replace(self._context, "")
        output_list = []
        for l in output:
            output_list.append(l)
            if l == "」":
                break
        output_sentence: str = "".join(output_list)
        self._context += output_sentence + "AI:「"
        next_utterance = output_sentence.replace("」", "")
        return next_utterance



