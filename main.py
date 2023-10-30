#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# main.py
#   automatically testing app
#   自動テスト用スクリプト

__version__ = '0.1'
__author__ = 'Mikio Nakano'
__copyright__ = 'C4A Research Institute, Inc.'


import argparse
from typing import Dict, Any, List
import yaml
import os, sys

from dialbb.main import DialogueProcessor
from chatgpt_tester_ja import ChatGPTTesterJa

DEFAULT_MAX_TURNS = 15
USER_ID = "user1"

if __name__ == '__main__':

    # read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--app_config", help="dialbb app config yaml file", required=True)
    parser.add_argument("--test_config", help="test_config", required=False)  # config
    parser.add_argument("--output", help="output file", required=False)  # output file (same format with test file)
    args = parser.parse_args()

    app_config_file: str = args.app_config
    dialogue_processor = DialogueProcessor(app_config_file)

    test_config_file: str = args.test_config
    test_config_dir: str = os.path.dirname(test_config_file)
    with open(test_config_file, encoding='utf-8') as fp:
        test_config: Dict[str, Any] = yaml.safe_load(fp)

    common_situation: str = test_config.get("common_situation", "")
    situations: List[str] = test_config.get("situations")
    if not situations:
        print("no situations are defined in the config.")
        sys.exit(1)
    generation_instructions: List[str] = test_config.get("generation_instructions")
    if not situations:
        print("no generation instructions are defined in the config.")
        sys.exit(1)
    temperatures: List[float] = test_config.get("temperatures", [0.7])

    user_simulator = ChatGPTTesterJa(test_config, test_config_dir)

    log_lines: List[str] = []

    max_turns = test_config.get('max_turns', DEFAULT_MAX_TURNS)

    # reads each user utterance from test input file and processes it

    if args.output:
        out_fp = open(args.output, mode='w', encoding='utf-8')
    else:
        out_fp = None

    for each_situation in situations:
        for generation_instruction in generation_instructions:
            for temperature in temperatures:

                situation: str = common_situation + each_situation

                user_simulator.set_parameters(situation, generation_instruction, temperature)

                num_turns: int = 0

                # first turn

                log_lines.append("----settings")
                log_lines.append("model: " + user_simulator.get_gpt_model())
                log_lines.append("situation: " + situation)
                log_lines.append("generation instruction: " + generation_instruction)
                log_lines.append("temperature: " + str(temperature))
                log_lines.append("----init")
                request = {"user_id": USER_ID}
                print("request: " + str(request))
                result = dialogue_processor.process(request, initial=True)
                print("response: " + str(result))
                print("SYS> " + result['system_utterance'])
                log_lines.append("System: " + result['system_utterance'])
                session_id = result['session_id']
                user_utterance = user_simulator.get_next_user_utterance(result['system_utterance'])

                while True:
                    num_turns += 1
                    print("USR> " + user_utterance)
                    log_lines.append("User: " + user_utterance)
                    request = {"user_id": USER_ID, "session_id": session_id,
                               "user_utterance": user_utterance}
                    print("request: " + str(request))
                    result = dialogue_processor.process(request, initial=False)
                    print("response: " + str(result))
                    print("SYS> " + result['system_utterance'])
                    log_lines.append("System: " + result['system_utterance'])
                    if result['final'] or num_turns >= max_turns:
                        break

                    # next utterance
                    user_utterance = user_simulator.get_next_user_utterance(result['system_utterance'])

                for log_line in log_lines:
                    print(log_line)

                if out_fp:
                    for log_line in log_lines:
                        print(log_line, file=out_fp)

                log_lines = []

    if out_fp:
        out_fp.close()


