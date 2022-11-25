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
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from dialbb.main import DialogueProcessor
from rinna_tester import RinnaTester

USER_ID = "user1"

if __name__ == '__main__':

    # read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="dialbb app config yaml file")
    parser.add_argument("situations", help="situation JSON file")  # test input file
    parser.add_argument("--model", help="model", required=False)  # output file (same format with test file)
    parser.add_argument("--output", help="output file", required=False)  # output file (same format with test file)
    args = parser.parse_args()

    with open(args.situations, encoding='utf-8') as fp:
        situations = json.load(fp)

    config_file: str = args.config
    dialogue_processor = DialogueProcessor(config_file)

    model_name: str = args.model
    if not model_name:
        model_name = "rinna-gpt-2"

    if model_name == "rinna-gpt-2":
        dialogue_tester = RinnaTester()
    else:
        print("unknown model:" + model_name)
        sys.exit(1)

    log_lines: List[str] = []
    session_id: str = ""

    # reads each user utterance from test input file and processes it
    for situation in situations:
        log_lines.append("----init")
        request = {"user_id": USER_ID}
        print("request: " + str(request))
        result = dialogue_processor.process(request, initial=True)
        print("response: " + str(result))
        print("SYS> " + result['system_utterance'])
        log_lines.append("System: " + result['system_utterance'])
        session_id = result['session_id']
        user_utterance = dialogue_tester.initialize_dialogue(situation, result['system_utterance'])
        while True:
            print("USR> " + user_utterance)
            log_lines.append("User: " + user_utterance)
            request = {"user_id": USER_ID, "session_id": session_id,
                       "user_utterance": user_utterance}
            print("request: " + str(request))
            result = dialogue_processor.process(request, initial=False)
            print("response: " + str(result))
            print("SYS> " + result['system_utterance'])
            log_lines.append("System: " + result['system_utterance'])
            if result['final']:
                break
            user_utterance = dialogue_tester.proceed_dialogue(result['system_utterance'])

    if args.output:
        with open(args.output, mode='w', encoding='utf-8') as fp:
            for log_line in log_lines:
                print(log_line, file=fp)


