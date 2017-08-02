# coding: utf-8

import requests
import json
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import default_reply
from lib import meiro

file = open('TOKENS.json', 'r')
fileContent = file.read()
file.close()
tokens = json.loads(fileContent)

@respond_to(r'^meiro(.*)')
def meiroResponce(message, arg):
    args = arg.split(r'\s')
    column = 100
    if len(args) > 1:
        column = parseInt(args[1], 100)

    filename = 'meiro.jpg'

    meiro1 = meiro.ImageMeiro(column, 480, filename)
    message.reply('creating a {0}*{0} maze...'.format(column))

    if meiro1.makeRoute():
        meiro1.save()
        data = {
            'token': tokens['legacy_token'],
            'channels': message.body['channel'],
            'filename': filename,
            'filetype': 'jpg',
            'title': filename
        }
        response = requests.post('https://slack.com/api/files.upload', data=data, files={'file': open(filename, 'rb')})
    else:
        message.reply('[error l58] Please adjust columns.')

def parseInt(string, initialvalue):
    try:
        return int(string)
    except ValueError:
        return initialvalue
