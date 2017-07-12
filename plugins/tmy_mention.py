# coding: utf-8

from slackbot.bot import Bot
from slackbot.bot import respond_to
from PIL import Image
import random
import itertools
import requests

class AbstractMeiro(object):
    MAX_ROUTE_SEARCH_COUNT = 20000
    def __init__(self, column, row, interval, boldness):
        self.column   = column   # horizontal pillars count plus 1
        self.row      = row      # vertical pillars count plus 1
        self.interval = interval # interval pixels
        self.boldness = boldness # width pixels of black line

        # unoccupied pillars, (x,y)s list
        self.pillarsUnoc = [(x,y) for x, y in itertools.product(xrange(1, column), xrange(1, row))] 
        # pillars temporarily used in specific phase
        self.pillarsUsed = []

    '''
    ()Z
    make meiro route
    '''
    def makeRoute(self):
        _count = 0
        pillar = (0,0)
        while True:
            if pillar == (0,0):
                pillar = self.getUnocPillarRandomly()
                self.pillarsUsed.append(pillar)
            pillar = self.makeNext(pillar)

            if len(self.pillarsUnoc) == 0:
                break
            # restrict loop for 20000 times
            _count += 1
            if _count > AbstractMeiro.MAX_ROUTE_SEARCH_COUNT:
                print('error l38: Too long it takes! Please adjust row or column.')
                ## debug ##
                # for pillar in self.pillarsUnoc:
                #    self.fillColor(pillar, pillar, (0, 255, 0))
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
        rand = random.randint(0, len(self.pillarsUnoc)-1)
        return self.pillarsUnoc[rand]

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

        for x, y in itertools.product(xrange(leftX, rightX), xrange(ceilY, bottomY)): 
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
        for y, x in itertools.product(xrange(0, height), xrange(0, width)): 
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

        for i, j in itertools.product(xrange(0, imgWidth), xrange(0, imgHeight)):
            self.img.putpixel((i,j), (255,255,255)) # make white canvas

    def fillColor(self, fromPillar, toPillar, color):
        leftX  = min(fromPillar[0], toPillar[0]) * (self.boldness + self.interval)
        rightX = max(fromPillar[0], toPillar[0]) * (self.boldness + self.interval) + self.boldness # -1
        ceilY   = min(fromPillar[1], toPillar[1]) * (self.boldness + self.interval)
        bottomY = max(fromPillar[1], toPillar[1]) * (self.boldness + self.interval) + self.boldness # -1

        for x, y in itertools.product(xrange(leftX, rightX), xrange(ceilY, bottomY)): 
            self.img.putpixel((x,y), color)

    '''
    ()V
    save as RGB image file
    '''
    def save(self):
        self.img.save(self.fileName)
        print('saved as '+self.fileName)

'''
r = 40
meiro1 = ImageMeiro(r, r, 480, 'meiro_{0}.jpg'.format(r))
if meiro1.makeRoute():
    meiro1.save()
'''

'''
meiro2 = StringMeiro(20, 20)
if meiro2.makeRoute():
    print(meiro2.save())
'''

@respond_to(r'^meiro+(.*)')
def slackBot(message, arg):
    args = arg.split(' ')[1:]
    column = 30
    row = 30
    mode = 'image'

    if len(args) == 1:
        column = parseInt(args[0], 20)
        row = column
    elif len(args) >= 2:
        column = parseInt(args[0], 20)
        row = parseInt(args[1], 20)
        if len(args) >= 3:
            mode = args[2]

    message.reply('creating a {0}*{1} maze...'.format(column, row))

    if mode == 'string':
        meiro = StringMeiro(column, row)
        flag = meiro.makeRoute()
        if flag:
            message.reply('\n'+meiro.save())
        else:
            message.reply('error l261: Too long it takes! Please adjust row or column.')
    elif mode == 'image':
        file = 'meiro.jpg'
        meiro = ImageMeiro(column, row, 480, file)
        if meiro.makeRoute():
            meiro.save()
            data = {
                'token': '0000-000000000000-000000000000-000000000000-00000000000000000000000000000000',
                'channels': message.body['channel'],
                'filename': file,
                'filetype': 'jpg',
                'title': file
            }
            response = requests.post('https://slack.com/api/files.upload', data=data, files={'file': open(file, 'rb')})

def parseInt(string, initialvalue):
    try:
        return int(string)
    except ValueError:
        return initialvalue
