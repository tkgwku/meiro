# coding: utf-8

from lib import meiro
from time import gmtime, strftime
import os
import argparse

parser = argparse.ArgumentParser(description = "-c/-column [integer] : the number of column, -s/-size [integer] : the pixel size of output image, -e/-entrancetype [0-3] : the entrances position preference")
parser.add_argument("-c", type=int, help = "-c/-column [integer] : the number of column", required=False)
parser.add_argument("-column", type=int, help = "-c/-column [integer] : the number of column", required=False)
parser.add_argument("-s", type=int, help = "-s/-size [integer] : the pixel size of output image", required=False)
parser.add_argument("-size", type=int, help = "-s/-size [integer] : the pixel size of output image", required=False)
parser.add_argument("-e", type=int, help = "-e/-entrancetype [0-3] : the entrances position preference", required=False)
parser.add_argument("-entrancetype", type=int, help = "-e/-entrancetype [0-3] : the entrances position preference", required=False)

command_arguments = parser.parse_args()

r = 100
px = 2000
et = 0

if command_arguments.c:
    r = command_arguments.c
if command_arguments.column:
    r = command_arguments.column
if command_arguments.s:
    px = command_arguments.s
if command_arguments.size:
    px = command_arguments.size
if command_arguments.e:
    et = command_arguments.e
if command_arguments.entrancetype:
    et = command_arguments.entrancetype

### Save As Image ###
directory = os.path.dirname('output/')
filename = directory+'/meiro_{0}_{1}.jpg'.format(r, strftime("%Y%m%d%H%M", gmtime()))
if not os.path.exists(directory):
    os.makedirs(directory)
meiro1 = meiro.ImageMeiro(r, px, filename, et)
if meiro1.makeRoute():
    if meiro1.DEBUG:
        print('[debug] costed {} counts'.format(meiro1.finishcount))
    meiro1.save()
