# coding: utf-8

from lib import meiro
from time import gmtime, strftime
import os

### Save As Image ###
r = 270
filename = 'output/meiro_{0}_{1}.jpg'.format(r, strftime("%Y%m%d%H%M", gmtime()))
directory = os.path.dirname('output/')
if not os.path.exists(directory):
    os.makedirs(directory)
meiro1 = meiro.ImageMeiro(r, 2000, filename)
if meiro1.makeRoute():
    if meiro1.DEBUG:
        print('{} counts'.format(meiro1.finishcount))
    meiro1.save()

'''
### debugging ###
r = '<table><tbody>\n<tr><th>column</th><th>count</th><th>ms</th><th>phases</th></tr>\n'
for col in range(100, 320, 10):
    analysis = meiro.AbstractMeiro(col, col, 1, 1)
    analysis.makeRoute()
    if analysis.finishcount > 0:
        r += '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>\n'.format(col, analysis.finishcount, analysis.ms, analysis.phaseCount)
r += '</tbody></table>'

f = open('table.txt', 'w')
f.write(r)
f.close()
'''