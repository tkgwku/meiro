# coding: utf-8

import sys
import os
import re
import argparse
from lib import meiro

# by https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description = "-c/-colortype [0-2] : gradation color type, -d/-drawanswer [True|False] : whether draw answer line; arguments are optional")
parser.add_argument("-c", type=int, help = "-c/-colortype [0-2] : gradation color type [0-3]", required=False)
parser.add_argument("-colortype", type=int, help = "-c/-colortype [0-2] : gradation color type [0-3]", required=False)
parser.add_argument("-d", type=str2bool, help = "-d/-drawanswer [True|False] : whether draw answer line [True|False]", required=False)
parser.add_argument("-drawanswer", type=str2bool, help = "-d/-drawanswer [True|False] : whether draw answer line [True|False]", required=False)

command_arguments = parser.parse_args()

colortype = 0
draw = True

if command_arguments.c:
    colortype = command_arguments.c
if command_arguments.colortype:
    colortype = command_arguments.colortype
if not command_arguments.d == None:
    draw = command_arguments.d
if not command_arguments.drawanswer == None:
    draw = command_arguments.drawanswer

sys.setrecursionlimit(100000)

directory = os.path.dirname('output/')
if not os.path.exists(directory):
    print('[error] there isn\'t \"output\" directory')
    quit()

directory2 = os.path.dirname('output/solution/')
if not os.path.exists(directory2):
    os.makedirs(directory2)
    
files = os.listdir(directory)
c = 0
for f in files:
    m = re.match(r'meiro_(.+)', f)
    if m:
        solutionpath = directory2+'/solutionmap_'+m.group(1)
        depthpath = directory2+'/depthmap_'+m.group(1)
        if (not os.path.exists(solutionpath)) or (not os.path.exists(depthpath)):
            solve1 = meiro.SolveMeiro(os.path.abspath(directory+'/'+f))
            if not os.path.exists(solutionpath):
                solve1.createSolutionMap(os.path.abspath(solutionpath))
                c += 1
            if not os.path.exists(depthpath):
                solve1.createDepthMap(os.path.abspath(depthpath), colortype, draw)
                c += 1

if c == 0:
    print('[info] No solution map or depth map is generated.')

