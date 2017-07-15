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

@respond_to(r'^meiro+(.*)')
def meiroResponce(message, arg):
    args = arg.split(' ')[1:]
    column = 40
    row = 40
    mode = 'image'

    if len(args) == 1:
        column = parseInt(args[0], 40)
        row = column
    elif len(args) >= 2:
        column = parseInt(args[0], 40)
        row = parseInt(args[1], 40)
        if len(args) >= 3:
            mode = args[2]

    if mode == 'string':
        meiro1 = meiro.StringMeiro(column, row)
        message.reply('creating a {0}*{1} maze...'.format(column, row))

        if meiro1.makeRoute():
            message.reply('\n'+meiro1.save())
        else:
            message.reply('[error l38] Please adjust row or column.')
    else:
        filename = 'meiro.jpg'

        meiro1 = meiro.ImageMeiro(column, row, 480, filename)
        message.reply('creating a {0}*{1} maze...'.format(column, row))

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
            meiro1.timerStop()
            message.reply('saved as {0} ({1} ms)'.format(filename, meiro1.ms))
        else:
            message.reply('[error l58] Please adjust row and column.')

def parseInt(string, initialvalue):
    try:
        return int(string)
    except ValueError:
        return initialvalue
