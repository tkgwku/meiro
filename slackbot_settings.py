# coding: utf-8

import json

file = open('TOKENS.json', 'r')
fileContent = file.read()
file.close()

try:
	tokens = json.loads(fileContent)
except Exception as e:
	raise

API_TOKEN = tokens['bot_token']

DEFAULT_REPLY = ""

PLUGINS = ['plugins']