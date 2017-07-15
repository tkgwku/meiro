# coding: utf-8

from lib import meiro

### Save As Image ###
r = 120
meiro1 = meiro.ImageMeiro(r, r, 1000, 'meiro_{0}.jpg'.format(r))
if meiro1.makeRoute():
    meiro1.timerStop()
    meiro1.save()

### Print As Text (Mac) ###
'''
meiro2 = StringMeiro(20, 20)
if meiro2.makeRoute():
    print(meiro2.save())
'''

### debug ###
'''
times = 5
for col in range(140, 155, 5):
    _a = []
    _ms = []
    for x in range(0,times):
        analysis = AbstractMeiro(col, col, 1, 1)
        analysis.makeRoute()
        if analysis.finishcount > 0:
            _a.append(analysis.finishcount)
            _ms.append(analysis.ms)
    ave = sum(_a) / len(_a)
    avems = sum(_ms) / len(_ms)
    print('<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td></tr>'.format(col, max(_a), min(_a), int(ave), max(_ms), min(_ms), avems))
'''
