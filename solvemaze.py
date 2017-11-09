# coding: utf-8

import sys
import os
import re
from lib import meiro

sys.setrecursionlimit(100000)

indir = os.path.dirname(os.path.abspath(__name__))
directory = os.path.dirname('output/')
if not os.path.exists(directory):
	print('there isn\'t \"output\" directory')
	quit()
files = os.listdir(directory)
meiros = list()
solves = list()
for f in files:
    if re.match(r'meiro_.+', f):
        meiros.append(f)
    elif re.match(r'solve_.+', f):
        solves.append(f[6:])

for meirofile in meiros:
    if not meirofile[6:] in solves:
        solve1 = meiro.SolveMeiro(indir+'/'+directory+'/'+meirofile, indir+'/'+directory+'/solve_'+meirofile[6:])
        solve1.solve()