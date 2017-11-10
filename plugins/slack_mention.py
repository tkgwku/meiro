# coding: utf-8

import requests
import json
import os
import sys
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import default_reply
from lib import meiro

file = open('TOKENS.json', 'r')
fileContent = file.read()
file.close()
tokens = json.loads(fileContent)

tempdir = '_temp/'
filename = 'meiro.jpg'
meiropath = tempdir+filename
solfilename = 'solve.jpg'
solpath = tempdir+solfilename

if not os.path.exists(tempdir):
    os.makedirs(tempdir)

sys.setrecursionlimit(100000)

@respond_to(r'^meiro(.*)')
def meiroResponce(message, arg):
    args = arg.split(r'\s')
    column = 100
    if len(args) > 1:
        column = parseInt(args[1], 100)

    meiro1 = meiro.ImageMeiro(column, 480, meiropath, 0)
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
        response = requests.post('https://slack.com/api/files.upload', data=data, files={'file': open(meiropath, 'rb')})
    else:
        message.reply('[error l44] Please adjust columns.')


@respond_to(r'^solve')
def solveResponce(message):
    if not os.path.exists(meiropath):
        message.reply('[error l55] Please make meiro first.')
    solve1 = meiro.SolveMeiro(os.path.abspath(meiropath))
    message.reply('creating a solution map...')
    solve1.createSolutionMap(os.path.abspath(solpath))
    data = {
        'token': tokens['legacy_token'],
        'channels': message.body['channel'],
        'filename': solfilename,
        'filetype': 'jpg',
        'title': solfilename
    }
    response = requests.post('https://slack.com/api/files.upload', data=data, files={'file': open(solpath, 'rb')})

def parseInt(string, initialvalue):
    try:
        return int(string)
    except ValueError:
        return initialvalue
