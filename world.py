# -*- coding: utf-8 -*-
__author__ = 'averrin'
import Image




class Tileset(dict):
    def __init__(self,dir):
        self.dir=dir
        self.signs={
         0:'1_3_0',
         1:'1_0_15',
         2:'1_1_14',
         3:'1_0_14',
         4:'1_5_14',
         5:'1_0_16',
         6:'1_5_16',
         7:'1_3_17',
         8:'1_3_17',
         9:'1_3_14',
         'none':' ',
         'door_closed_v':'2_2_10',
         'door_open_v':'1_0_18',
         'door_closed_h':'2_2_10',
         'door_open_h':'1_0_18',
         'window_v':'1_1_20',
         'window_h':'1_1_20',
        }
        self.load()

    def load(self):
        infile=['tilesets/%s/%s.bmp' % (self.dir,i) for i in xrange(3)]
        for i,fname in enumerate(infile):
            try:
                im = Image.open(fname)
                xsize,ysize=im.size
                for row in xrange(31):
                    for col in xrange(7):
                        box = ((xsize/8)*col ,(ysize/32)*row, (xsize/8)*(col+1), (ysize/32)*(row+1))
                        region = im.crop(box)
                        region.save('tilesets/.temp/%d_%d_%d.png' % (i,col,row), "png")
            except Exception,e:
                print e
        try:
            im = Image.open('tilesets/%s/chars.png'%self.dir)
            xsize,ysize=im.size
            for row in xrange(31):
                for col in xrange(15):
                    box = ((xsize/32)*col ,(ysize/16)*row, (xsize/32)*(col+1), (ysize/16)*(row+1))
                    region = im.crop(box)
                    region.save('tilesets/.temp/char_%d_%d.png' % (col,row), "png")
        except Exception,e:
            print e

    def __getitem__(self, item):
        try:
            return 'tilesets/.temp/%s.png' % self.signs[item]
        except:
            return 'tilesets/.temp/%s.png' % item

TILESET=Tileset('default')

class Tile(object):
    def __init__(self,x=0,y=0,type='none'):
        self.type=type
        self.x=x
        self.y=y
        self.coords=(x,y)
        self.desc=''
        self.gdesc=''
        self.sign=''
        self.char=''
        self.layers=[]
        self.items=[]

    def chType(self,type):
#        if self.type=='none':
#            self.layers[0]=TILESET[type]
#        else:
        self.layers.append(TILESET[type])
        self.type=type

    def getBackground(self):
        return self.layers[0]

    def get(self,d):
        WORLD=self.stage
        if d=='n':
            return WORLD.get(self.x,self.y-1)
        elif d=='s':
            return WORLD.get(self.x,self.y+1)
        elif d=='w':
            return WORLD.get(self.x-1,self.y)
        elif d=='e':
            return WORLD.get(self.x+1,self.y)
        else:
            return ''

    def onCome(self):
        if not self.char:
            return True
        else:
            self.char.onTouch()
            return False

    def setChar(self,char=''):
        self.char=char
        if char:
            self.layers.append(char.sign)
            self.onCharEnter()
            char.coord=(self.x,self.y)
            char.tile=self
        else:
            self.layers.remove(self.layers[-1])
            self.onCharLeave()
#        print 'char added',self.layers, self.items
        self.stage.core.drawTile(self)

    def onCharEnter(self):
        self.stage.core.drawTile(self)
    def onCharLeave(self):
        self.stage.core.drawTile(self)

    def __str__(self):
        return self.layers

    def info(self):
        return self.__class__.__name__, self.type, self.char.Name if self.char else '', self.__str__(), 'items:',len(self.items)

class Wall(Tile):
    def __init__(self,x=0,y=0,type='v'):
        Tile.__init__(self,x,y,{'h':1,'v':2}[type])
        self.chType(self.type)

    def onCome(self):
        return False


class Window(Tile):
    def __init__(self,x=0,y=0,type='v'):
        Tile.__init__(self,x,y,{'h':'window_h','v':'window_v'}[type])
#        self.layers[0]=TILESET[self.type]
        self.chType(self.type)

    def onCome(self):
        self.stage.core.app['print'](u'Ухты-йопты, окно!')
        return False

class Door(Tile):
    def __init__(self,x=0,y=0,type='v',closed=False,locked=False,lock_force=0):
        self.closed=closed
        self.locked=locked
        self.d=type
        Tile.__init__(self,x,y,{'h':{False:'door_open_h',True:'door_closed_h'},'v':{False:'door_open_v',True:'door_closed_v'}}[self.d][closed])
        self.layers.append(TILESET['door_open_h'])
        if closed:
            self.chType({'h':{False:'door_open_h',True:'door_closed_h'},'v':{False:'door_open_v',True:'door_closed_v'}}[self.d][self.closed])

    def onCome(self):
        return self.open()

    def open(self):
        if self.closed:
            if not self.locked:
                self.closed=False
                self.chType({'h':{False:'door_open_h',True:'door_closed_h'},'v':{False:'door_open_v',True:'door_closed_v'}}[self.d][self.closed])
            else:
                self.stage.core.app['print'](u'Заперто!')

            self.stage.core.drawTile(self)
            return False
        else:
            self.stage.core.drawTile(self)
            return True

    def onCharLeave(self):
        Tile.onCharLeave(self)
        self.close()

    def close(self):
        self.closed=True
        self.chType({'h':{False:'door_open_h',True:'door_closed_h'},'v':{False:'door_open_v',True:'door_closed_v'}}[self.d][self.closed])
        self.stage.core.drawTile(self)



class Matrix(list):
    def __init__(self,rows=1,columns=0,room=False):
        self.rows=rows
        self.columns=columns
        for i in xrange(self.rows):
            self.append([])
            for c in xrange(self.columns):
                t=Tile(c,i)
                t.stage=self
                self[i].append(t)
        if room:
            for i,row in enumerate(self):
                if not i or i == self.rows-1:
                    for c,t in enumerate(row):
                        row[c]=Wall(c,i,'v')
#                        row[0]=Wall(c,i,'v')
#                        row[-1]=Wall(c,i,'v')
                    if not i:
                        row[0].chType(3)
                        row[-1].chType(4)
                    else:
                        row[0].chType(5)
                        row[-1].chType(6)
                else:
                    for ii,t in enumerate(row):
                        t.chType(0)
                    row[0]=Wall(c,i,'h')
                    row[-1]=Wall(c,i,'h')

    def getList(self):
        __list=[]
        for row in self:
            __list.append(row[:])
        return __list

    def get(self,x,y):
        try:
            return self[y][x]
        except:
            return ''

    def set(self,x,y,tile):
        #TODO: implement add* on except
        tile.x=x
        tile.y=y
        tile.stage=self
        self[y][x]=tile

    def addRow(self):
        self.append([])
        for c in xrange(self.columns):
            self[len(self)-1].append(Tile(c,len(self)-1))

    def addColumn(self):
        for i,row in enumerate(self):
            row.append(Tile(len(row),i))

    def addVWall(self,x,start=0,end=0):
        if not end:
            end=self.rows-1
        for i,row in enumerate(self):
            if i in range(start,end) and i!=0 and i!=self.rows-1:
                row[x]=Wall(row[x].x,row[i].y,'h')
            elif not i:
                row[x].chType(9)
            elif i==self.rows-1:
                row[x].chType(7)

    def addHWall(self,y,start=0,end=0):
        if not end:
            end=self.columns-1
        row=self[y]
        for i,t in enumerate(row):
            if i in range(start,end) and i!=0 and i!=self.columns-1:
                row[i]=Wall(t.x,t.y,'v')


    def fillArea(self,tl,br,type):
        area=self
        for row in area:
            if row[0].y in range(tl[1],br[1]):
                for t in row:
                    if t.x in range(tl[0],br[0]):
                        if type in TILESET:
                            t.chType(type)
                        else:
                            t.sign=type

    def removeArea(self,tl,br):
        self.fillArea(tl,br,'none')

    def __str__(self):
        __str=''
        for row in self:
            __row=''
            for t in row:
                __row+=str(t)
            __str+=__row+'<br>'
        return __str

class Room(list):
    def __init__(self,tiles,tl,br,title=''):
        self.title=title
        area=tiles[:]
        area=area[:br[1]]
        for row in area:
            for t in reversed(row):
                if t.x > br[0]:
                    row.remove(t)
        for row in reversed(area):
            if row[0].y<tl[1]:
                area.remove(row)
            for t in reversed(row):
                if t.x<tl[0]:
                    row.remove(t)
        self.extend(area)

    def __str__(self):
        __str=''
        for row in self:
            __row=''
            for t in row:
                __row+=str(t)
            __str+=__row+'\n'
        return __str


def main():
    stage=Matrix(16,30,room=True)
#    stage.set(6,4,Tile(type='hero'))
    stage.addHWall(6)
    stage.addHWall(8,end=15)
    stage.addVWall(15)
    stage[6][15].chType(9)
    stage.set(15,4,Door(type='v'))
    stage.set(15,7,Door(type='v',closed=True))
    stage.set(3,6,Door(type='h'))
    stage.set(18,6,Door(type='h',closed=True))
    stage.set(12,8,Door(type='h',closed=True,locked=True))
    stage.set(0,4,Window(type='v'))
    stage.set(0,5,Window(type='v'))
    stage.set(4,0,Window(type='h'))
#    stage.set(3,0,Window(type='h'))
    rooms=[]
    rooms.append(Room(stage.getList(),(0,0),(15,7),'Your room'))
    rooms.append(Room(stage.getList(),(15,0),(35,7),'Kiro room'))
    rooms.append(Room(stage.getList(),(15,6),(35,16),'Main hall'))
    rooms.append(Room(stage.getList(),(0,8),(15,16),'Hall'))
    stage.rooms=rooms
#    stage.removeArea((2,12),(14,14))
#    stage.fillArea((2,12),(14,14),'<span style="color:red;background:cyan;">*</span>')
#    stage[4][7].sign='<img src="icons/real_poison.png" width="8">'
#    print stage
    return stage
#    t=stage.get(0,0).get('bottom')
#    for i in xrange(30):
#        t=t.get('left')
#        print t.coords

if __name__ == '__main__':
    main()