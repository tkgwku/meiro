# coding: utf-8

import sys
import os
import re
from lib import meiro

sys.setrecursionlimit(100000)

directory = os.path.dirname('output/')
if not os.path.exists(directory):
    print('there isn\'t \"output\" directory')
    quit()

directory2 = os.path.dirname('output/solution/')
if not os.path.exists(directory2):
    os.makedirs(directory2)
    
files = os.listdir(directory)
for f in files:
    m = re.match(r'meiro_(.+)', f)
    if m:
        solutionpath = directory2+'/solutionmap_'+m.group(1)
        depthpath = directory2+'/depthmap_'+m.group(1)
        if (not os.path.exists(solutionpath)) or (not os.path.exists(depthpath)):
            solve1 = meiro.SolveMeiro(os.path.abspath(directory+'/'+f))
            if not os.path.exists(solutionpath):
                solve1.createSolutionMap(os.path.abspath(solutionpath))
            if not os.path.exists(depthpath):
                solve1.createDepthMap(os.path.abspath(depthpath), 0, True)
                #solve1.createDepthMap(os.path.abspath(depthpath), 2, False)