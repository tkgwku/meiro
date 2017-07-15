# coding: utf-8

import itertools
import random
import time
import math
from PIL import Image

class AbstractMeiro(object):
    DEBUG = True

    def __init__(self, column, row, interval, boldness):
        self.column   = column   # horizontal pillars count plus 1
        self.row      = row      # vertical pillars count plus 1
        self.interval = interval # interval pixels
        self.boldness = boldness # width pixels of black line

        # unoccupied pillars, (x,y)s list
        self.pillarsUnoc = [(x,y) for x, y in itertools.product(range(1, column), range(1, row))]
        # pillars temporarily used in specific phase
        self.pillarsUsed = []
        # seconds it will take
        self.expectedSec = self.getExpectedSecond()
        # how many times loop is executed to make meiro
        self.finishcount = 0
        # how long it takes to make meiro
        self.ms = 0

    '''
    ()Z
    make meiro route
    '''
    def makeRoute(self):
        if self.column < 0 or self.row < 0 or self.column > 150 or self.row > 150:
            print('error l39: Invalid argument!')
            return False
        _count = 0
        pillar = (0,0)
        self.timerStart()
        maxSearchCount = self.getMaxSearchCount()
        print('starting {0}*{1} meiro making... it will take {2} seconds...'.format(self.column, self.row, self.expectedSec))
        while True:
            if pillar == (0,0):
                pillar = self.getUnocPillarRandomly()
                self.pillarsUsed.append(pillar)
            pillar = self.makeNext(pillar)

            if len(self.pillarsUnoc) == 0:
                self.finishcount = _count
                break
            # restrict loop for 20000 times
            _count += 1
            if _count > maxSearchCount:
                print('[error l61] Something went wrong!')
                ## debug ##
                if AbstractMeiro.DEBUG:
                    for pillar in self.pillarsUnoc:
                        self.fillColor(pillar, pillar, (0, 255, 0))
                    break
                return False

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
    def makeNext(self, currentPillar):
        nextPillar = self.getNextPillar(currentPillar)
        state = self.getWallMakingState(nextPillar)
        self.pillarsUsed.append(nextPillar)
        if state == State.ABORT:
            self.pillarsUsed = []
            return (0,0)
        elif state == State.SAVE:
            self.saveChanges()
            return (0,0)
        elif state == State.KEEP:
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
                self.pillarsUnoc.remove(pillar)
        self.pillarsUsed = []

    def getUnocPillarRandomly(self):
        return self.pillarsUnoc[random.randint(0, len(self.pillarsUnoc)-1)]

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

    '''
    (tuple2)tuple2
    randomly select from pillars next to current one
    '''
    def getNextPillar(self, currentPillar):
        direction = random.randint(0, 3) # 0:up 1:down 2:left 3:right
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
        flag = pillar[0] == 0
        flag = flag or pillar[1] == 0
        flag = flag or pillar[0] == self.column
        flag = flag or pillar[1] == self.row
        return flag

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
    (int, int, int)int
    calculate proper boldness and interval from column, row and size
    '''
    def getProperBoldness(self, column, row, size):
        return int( size / ( 2*max(column, row)+1 )) +1

    '''
    ()int
    get expected number of max search count
    '''
    def getMaxSearchCount(self):
        x = math.sqrt(self.column * self.row)
        return int(0.2258 * math.pow(x, 2.8508) + 25000)

    '''
    ()float
    get expectation about how long while-loop takes
    '''
    def getExpectedSecond(self):
        x = math.sqrt(self.column * self.row)
        return int(0.00000012 * math.pow(x, 4.4769)) / 10

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
meiro made of strings
'''
class StringMeiro(AbstractMeiro):
    def __init__(self, column, row):
        super(StringMeiro, self).__init__(column, row, 1, 1)
        self.blocks = []

    def fillColor(self, fromPillar, toPillar, color):
        leftX  = min(fromPillar[0], toPillar[0]) * (self.boldness + self.interval)
        rightX = max(fromPillar[0], toPillar[0]) * (self.boldness + self.interval) + self.boldness # -1
        ceilY   = min(fromPillar[1], toPillar[1]) * (self.boldness + self.interval)
        bottomY = max(fromPillar[1], toPillar[1]) * (self.boldness + self.interval) + self.boldness # -1

        for x, y in itertools.product(range(leftX, rightX), range(ceilY, bottomY)):
            self.blocks.append((x,y))

    '''
    ()String
    return string meiro
    @override
    '''
    def save(self):
        result = ''
        width  = self.column * self.interval + (self.column + 1) * self.boldness # image width
        height = self.row    * self.interval + (self.row    + 1) * self.boldness # image height
        for y, x in itertools.product(range(0, height), range(0, width)):
            if (x,y) in self.blocks:
                result += '⬛'
            else:
                result += '⬜'
            if x == width-1:
                result += '\n'
        return result


'''
meiro saved as image
'''
class ImageMeiro(AbstractMeiro):
    def __init__(self, column, row, size, fileName):
        prop = self.getProperBoldness(column, row, size)
        super(ImageMeiro, self).__init__(column, row, prop, prop)

        self.fileName = fileName

        imgWidth  = column * self.interval + (column + 1) * self.boldness # image width
        imgHeight = row    * self.interval + (row    + 1) * self.boldness # image height
        self.img = Image.new('RGB', (imgWidth, imgHeight)) # canvas

        for i, j in itertools.product(range(0, imgWidth), range(0, imgHeight)):
            self.img.putpixel((i,j), (255,255,255)) # make white canvas

    def fillColor(self, fromPillar, toPillar, color):
        leftX  = min(fromPillar[0], toPillar[0]) * (self.boldness + self.interval)
        rightX = max(fromPillar[0], toPillar[0]) * (self.boldness + self.interval) + self.boldness # -1
        ceilY   = min(fromPillar[1], toPillar[1]) * (self.boldness + self.interval)
        bottomY = max(fromPillar[1], toPillar[1]) * (self.boldness + self.interval) + self.boldness # -1

        for x, y in itertools.product(range(leftX, rightX), range(ceilY, bottomY)):
            self.img.putpixel((x,y), color)

    '''
    ()V
    save as RGB image file
    '''
    def save(self):
        self.img.save(self.fileName)
        print('saved as {0}'.format(self.fileName, self.ms))
