# coding: utf-8

import itertools
import random
import time
import math
from PIL import Image

class AbstractMeiro(object):
    DEBUG = False

    def __init__(self, column, row, interval, boldness):
        self.column   = column   # horizontal pillars count plus 1
        self.row      = row      # vertical pillars count plus 1
        self.interval = interval # interval pixels
        self.boldness = boldness # width pixels of black line

        # unoccupied pillars, (x,y)s list
        self.pillarsUnoc = []
        # pillars temporarily used in specific phase
        self.pillarsUsed = []
        # how many times loop is executed to make meiro
        self.finishcount = 0
        # how long it takes to make meiro
        self.ms = 0
        self.timerStart()

        # parameter 1
        #self.phaseCount = int(max(column, row)/20)
        self.phaseCount = int(max(column, row)/40)

        self.phaseUnoc = [[] for i in range(0, self.phaseCount-1)]#[[],[]]
            
        for i, j in itertools.product(range(1, column), range(1, row)):
            self.pillarsUnoc.append((i,j))
            for k in range(0, self.phaseCount-1):#0,1
                if self.isIn(i, j, k+1):
                    self.phaseUnoc[k].append((i,j))
                    break

        self.phaseLen = [len(x) for x in self.phaseUnoc]

    def isIn(self, i, j, k):
        return min(i, self.column-i) < k*self.column/(2*self.phaseCount) or min(j, self.row-j) < k*self.row/(2*self.phaseCount)

    '''
    ()Z
    make meiro route
    '''
    def makeRoute(self):
        if self.column < 0 or self.row < 0:
            print('error: Invalid argument!')
            return False

        _count = 0
        pillar = (0,0)
        prevDir = -1
        phase = 0
        maxSearchCount = 1000000
        print('starting {0}*{1} meiro making...'.format(self.column, self.row))
        while True:
            if phase < self.phaseCount-1 and len(self.phaseUnoc[phase]) < self.phaseLen[phase]/5: # parameter 2
                phase += 1
                print('phase {0}/{1}... ({2} sec)'.format(phase, self.phaseCount-1, int(time.time() * 100 - self.ms/10)/100))

            if pillar == (0,0):
                pillar = self.getUnocPillarRandomly(phase)
                self.pillarsUsed.append(pillar)
                prevDir = -1

            direction = self.makeNewDirection(prevDir)
            prevDir = direction
            pillar = self.makeNext(pillar, direction)

            if len(self.pillarsUnoc) == 0:
                self.finishcount = _count
                break

            _count += 1
            if _count > maxSearchCount:
                print('[error l61] Something went wrong!')
                ## debug ##
                if AbstractMeiro.DEBUG:
                    for pillar in self.pillarsUnoc:
                        self.fillColor(pillar, pillar, (0, 255, 0))
                    break
                return False
        self.timerStop()
        if AbstractMeiro.DEBUG:
            print('{} seconds'.format(self.ms/1000))
        # make edge wall
        self.draw((0,0), (0, self.row))
        self.draw((0,0), (self.column-1, 0))
        self.draw((self.column,0), (self.column, self.row))
        self.draw((1,self.row), (self.column, self.row))
        return True

    '''
    ()V
    save meiro in some way
    @abstractmethod
    '''
    def save(self):
        pass

    '''
    (tuple2)tuple2
    process the next pillar
    '''
    def makeNext(self, currentPillar, direction):
        nextPillar = self.getNextPillar(currentPillar, direction)
        state = self.getWallMakingState(nextPillar)
        if state == State.ABORT:
            if AbstractMeiro.DEBUG:
                self.debugSave()
            self.pillarsUsed = []
            return (0,0)
        elif state == State.SAVE:
            self.pillarsUsed.append(nextPillar)
            self.saveChanges()
            return (0,0)
        elif state == State.KEEP:
            self.pillarsUsed.append(nextPillar)
            return nextPillar

    '''
    ()V
    turn temporary pillars into wall
    '''
    def saveChanges(self):
        for (i, pillar) in enumerate(self.pillarsUsed):
            if i <= len(self.pillarsUsed) -2:
                self.draw(pillar, self.pillarsUsed[i+1])
            if pillar in self.pillarsUnoc:
                self.rm(pillar)
        self.pillarsUsed = []

    def rm(self, pillar):
        self.pillarsUnoc.remove(pillar)
        temp = []
        for phase in self.phaseUnoc:
            if pillar in phase:
                phase.remove(pillar)
            temp.append(phase)
        self.phaseUnoc = temp
        del temp

    '''
    ()V
    turn temporary pillars into wall
    '''
    def debugSave(self):
        for (i, pillar) in enumerate(self.pillarsUsed):
            if i <= len(self.pillarsUsed) -2:
                self.fillColor(pillar, self.pillarsUsed[i+1], (255, 0, 0))

    def getUnocPillarRandomly(self, phase):
        tar = self.phaseUnoc[phase] if phase < self.phaseCount-1 else self.pillarsUnoc
        return tar[random.randint(0, len(tar)-1)]

    '''
    (tuple2, tuple2, tuple3)V
    fill canvas with certain color, from pillar to pillar
    @abstractmethod
    '''
    def fillColor(self, fromPillar, toPillar, color):
        pass

    '''
    (tuple2, tuple2)V
    draw line on canvas, from pillar to pillar
    '''
    def draw(self, fromPillar, toPillar):
        self.fillColor(fromPillar, toPillar, (60, 60, 60))

    def makeNewDirection(self, prev):
        # 0:up 1:down 2:left 3:right
        if prev == -1:
            return random.randint(0, 3)
        else:
            _dirs = [1, 0 ,3, 2]
            del _dirs[prev]
            return _dirs[random.randint(0, 2)]

    '''
    (tuple2)tuple2
    randomly select from pillars next to current one
    '''
    def getNextPillar(self, currentPillar, direction):
        # go up
        if direction == 0:
            return (currentPillar[0], currentPillar[1]-1)
        # go down
        elif direction == 1:
            return (currentPillar[0], currentPillar[1]+1)
        # go left
        elif direction == 2:
            return (currentPillar[0]-1, currentPillar[1])
        # go right
        elif direction == 3:
            return (currentPillar[0]+1, currentPillar[1])

    '''
    (tuple2)Z
    return whether the pillar is already occupied, completed as wall
    '''
    def isOccupied(self, pillar):
        return pillar not in self.pillarsUnoc

    '''
    (tuple2)Z
    return whether the pillar is at edge wall
    '''
    def isAtEdge(self, pillar):
        return pillar[0] == 0 or pillar[1] == 0 or pillar[0] == self.column or pillar[1] == self.row

    '''
    (tuple2)State
    get the condition the pillars in
     - ABORT means they will be aborted
     - SAVE means they will survive
     - KEEP means their destiny have yet to be determined
    '''
    def getWallMakingState(self, nextPillar):
        if nextPillar in self.pillarsUsed:
            return State.ABORT
        elif self.isOccupied(nextPillar) or self.isAtEdge(nextPillar):
            return State.SAVE
        else:
            return State.KEEP

    '''
    ()V
    start timer
    '''
    def timerStart(self):
        self.ms = int(time.time() * 1000)

    '''
    ()V
    stop timer
    '''
    def timerStop(self):
        self.ms = int(time.time() * 1000) - self.ms



class State():
    ABORT = 1
    SAVE  = 2
    KEEP  = 3

'''
meiro saved as image
'''
class ImageMeiro(AbstractMeiro, object):
    def __init__(self, columns, size, fileName):
        super(ImageMeiro, self).__init__(columns, columns, 1, 1)

        self.fileName = fileName

        width = 2 * columns + 1
        self.magn = (int(size/width) + 1) * width
        self.img = Image.new('RGB', (width, width)) # canvas

        for i, j in itertools.product(range(0, width), range(0, width)):
            self.img.putpixel((i,j), (255,255,255)) # make white canvas

    def fillColor(self, fromPillar, toPillar, color):
        leftX  = min(fromPillar[0], toPillar[0]) * 2
        rightX = max(fromPillar[0], toPillar[0]) * 2 + 1 # -1
        ceilY   = min(fromPillar[1], toPillar[1]) * 2
        bottomY = max(fromPillar[1], toPillar[1]) * 2 + 1 # -1

        for x, y in itertools.product(range(leftX, rightX), range(ceilY, bottomY)):
            self.img.putpixel((x,y), color)

    '''
    ()V
    save as RGB image file
    '''
    def save(self):
        self.img = self.img.resize((self.magn, self.magn))
        self.img.save(self.fileName)
        print('saved as {0} ({1}*{1} pixel)'.format(self.fileName, self.magn))


class SolveMeiro(object):
    def __init__(self, path):
        print('[load] {} ...'.format(path))
        img = Image.open(path, 'r')
        width, height = img.size
        print('[info] width: {1}px, height: {2}px'.format(path, width, height))

        boldness = 0

        for x in range(0, width):
            if not self.isBlack(img.getpixel((x, height-1))):
                if x == 0:
                    print('error l33')
                    quit()
                else:
                    boldness = x
                    break

        self.xlen = int(width/boldness)
        self.ylen = int(height/boldness)

        print('[info] column: {0}, row: {1}'.format(int((self.ylen-1)/2), int((self.xlen-1)/2)))
        self.blocks = dict()

        #debug_string_array = ['' for i in range(0, self.ylen)]

        for i, j in itertools.product(range(0, self.xlen), range(0, self.ylen)):
            self.blocks[(i,j)] = 0 if self.isWall((i,j), img, boldness) else 1 # 0 means that area plays role of wall
            #debug_string_array[j] += '_' if not self.isWall((i,j)) else 'X'

        #debugStr = ''
        #for line in debug_string_array:
        #    debugStr += line + '\n'

        #print(debugStr)

        self.goal = (self.xlen-2, 0)

    def createSolutionMap(self, filename):
        self.intersections = list()
        self.loadintersections((1, self.ylen-1), (0, self.ylen), (1, self.ylen-1), 0)
        self.save(filename)

    def isBlack(self, rgb):
        return rgb[0] < 120 and rgb[1] < 120 and rgb[2] < 120

    def isWall(self, block, img, boldness):
        sampleX = (block[0] + 0.5) * boldness
        sampleY = (block[1] + 0.5) * boldness

        sampleX = int(sampleX)
        sampleY = int(sampleY)

        return self.isBlack(img.getpixel((sampleX,sampleY)))

    def leftOf(self, coord):
        return (coord[0]-1, coord[1])

    def rightOf(self, coord):
        return (coord[0]+1, coord[1])

    def forwardOf(self, coord):
        return (coord[0], coord[1]-1)

    def backwardOf(self, coord):
        return (coord[0], coord[1]+1)

    def getcoord(self, coord, dirId):
        if dirId == 0:
            return self.forwardOf(coord)
        elif dirId == 1:
            return self.rightOf(coord)
        elif dirId == 2:
            return self.backwardOf(coord)
        else:
            return self.leftOf(coord)

    def isout(self, coord):
        return coord[0] < 0 or coord[0] >= self.ylen or coord[1] < 0 or coord[1] >= self.xlen

    def loadintersections(self, coord, fromCoord, previs, prevdir):
        nexts = list()

        for x in range(0,4):
            c = self.getcoord(coord, x)
            if self.isout(c) or c == fromCoord:
                continue
            elif self.blocks[c] == 1: # space
                nexts.append(x)

        # 通行路
        if len(nexts) == 1:
            if self.getcoord(coord, nexts[0]) == self.goal:
                tup = (self.goal, previs, prevdir)
                self.intersections.append(tup)
                # print(intersections)
            else:
                self.loadintersections(self.getcoord(coord, nexts[0]), coord, previs, prevdir)
        # 行き止まり
        elif len(nexts) == 0:
            pass
        # 交差点
        elif len(nexts) > 1:
            tup = (coord, previs, prevdir)
            self.intersections.append(tup)
            for nextdir in nexts:
                if self.getcoord(coord, nextdir) == self.goal:
                    tup = (self.goal, coord, nextdir)
                    self.intersections.append(tup)
                    # print(intersections)
                else:
                    self.loadintersections(self.getcoord(coord, nextdir), coord, coord, nextdir)

    def save(self, filename):
        img2 = Image.new('RGB', (self.xlen, self.ylen))

        for x, y in itertools.product(range(0, self.xlen), range(0, self.ylen)):
            if self.blocks[(x,y)] == 1:
                img2.putpixel((x,y), (255,255,255))
            else:
                img2.putpixel((x,y), (60,60,60))

        #print(intersections)

        self.tploop(self.goal, img2, (255,0,150))

        img2 = img2.resize((self.getmgnx(), self.getmgny()))
        img2.save(filename)
        print('[success] saved solution map.')

    def drawline(self, tpl, img2, rgb):
        to = tpl[0]
        fro = tpl[1]
        dire = tpl[2]
        img2.putpixel(fro, rgb)
        c1 = self.getcoord(fro, dire)
        self.loop(c1, fro, to, img2, rgb)

    def loop(self, coord, fromCoord, to, img2, rgb):
        if coord == to:
            img2.putpixel(to, rgb)
        else:
            for x in range(0,4):
                c2 = self.getcoord(coord, x)
                if self.isout(c2) or c2 == fromCoord:
                    pass
                elif c2 == to:
                    img2.putpixel(coord, rgb)
                    img2.putpixel(to, rgb)
                elif self.blocks[c2] == 1: # space
                    img2.putpixel(coord, rgb)
                    self.loop(c2, coord, to, img2, rgb)

    def tploop(self, coord, img2, rgb):
        for tpl in self.intersections:
            if tpl[0] == coord:
                self.drawline(tpl, img2, rgb)
                self.tploop(tpl[1], img2, rgb)

    def getmgnx(self):
        return int(2000/self.xlen)*self.xlen

    def getmgny(self):
        return int(2000/self.ylen)*self.ylen

    def createDepthMap(self, depthfilename, gradationtype, drawsolution):
        self.depthMap = dict()
        self.depthMapLoop((1, self.ylen-1), (0, 0), 0)
        img2 = Image.new('RGB', (self.xlen, self.ylen))
        maxdepth = max(self.depthMap.values())
        for x, y in itertools.product(range(0, self.xlen), range(0, self.ylen)):
            if self.blocks[(x,y)] != 1:
                img2.putpixel((x,y), (60,60,60))
            elif (x,y) in self.depthMap:
                i = self.depthMap[(x,y)]
                img2.putpixel((x,y), self.lineargradation(i, maxdepth, gradationtype))
            else:
                img2.putpixel((x,y), (255,255,255))
        if drawsolution:
            linecolors = [(255,0,150),(255,0,150),(4, 4, 219)]
            self.intersections = list()
            self.loadintersections((1, self.ylen-1), (0, self.ylen), (1, self.ylen-1), 0)
            self.tploop(self.goal, img2, linecolors[gradationtype])
        img2 = img2.resize((self.getmgnx(), self.getmgny()))
        img2.save(depthfilename)
        print('[success] saved depth map.')

    def depthMapLoop(self, coord, fromCoord, depth):
        nexts = list()

        self.depthMap[coord] = depth

        for x in range(0,4):
            c = self.getcoord(coord, x)
            if self.isout(c) or c == fromCoord:
                continue
            elif self.blocks[c] == 1: # space
                nexts.append(x)

        # 行き止まり
        if len(nexts) == 0:
            pass
        # 交差点
        elif len(nexts) >= 1:
            for nextdir in nexts:
                if self.getcoord(coord, nextdir) == self.goal:
                    self.depthMap[self.goal] = depth+1
                else:
                    self.depthMapLoop(self.getcoord(coord, nextdir), coord, depth+1)

    def lineargradation(self, i, m, gradationtype):
        grads = [
            [(181, 102, 255),(102, 191, 255),(42, 135, 0),(255, 255, 0),(234, 16, 74)],
            [(75,0,130),(0,0,255),(0,255,0),(255,255,0),(255,127,0),(255,0,0)],
            [(0,255,255),(255,255,255),(255,0,255)]
        ]
        colors = grads[gradationtype]
        l = len(colors)-1
        ratio = i/m
        for x in range(0,l):
            if ratio >= x/l and ratio <= (x+1)/l:
                beg = colors[x]
                end = colors[x+1]
                rat = (ratio*l)%1
                r = (end[0]-beg[0])*rat+beg[0]
                g = (end[1]-beg[1])*rat+beg[1]
                b = (end[2]-beg[2])*rat+beg[2]
                return (int(r),int(g),int(b))


            
