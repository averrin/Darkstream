# -*- coding: utf-8 -*-
__author__ = 'averrin'


TILESET={0:'<span style="color:#111;">.</span>',1:'▉',2:'■',3:'■',
         'none':' ',
         'hero':'<span style="color:green;">◐</span>',
         'door_closed_v':'|',
         'door_open_v':'/',
         'door_closed_h':'-',
         'door_open_h':'/',
         'window_v':'<span style="color:blue;">‖</span>',
         'window_h':'<span style="color:blue;">=</span>',
        }

class Tile(object):
    def __init__(self,x=0,y=0,type='none'):
        self.type=type
        self.x=x
        self.y=y
        self.coords=(x,y)
        self.desc=''
        self.gdesc=''
        self.sign=''

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

    def __str__(self):
        if not self.sign:
            return TILESET[self.type]
        else:
            return self.sign
#        return '(%s,%s)' % (str(self.x).zfill(2),str(self.y).zfill(2))

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
                    for t in row:
                        t.type=2
                        row[0].type=3
                        row[-1].type=3
                else:
                    for ii,t in enumerate(row):
                        t.type=0
                    row[0].type=1
                    row[-1].type=1

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

    def addHWall(self,x,start=0,end=0):
        if not end:
            end=self.rows-1
        for i,row in enumerate(self):
            if i in range(start,end) and i!=0 and i!=self.rows-1:
                row[x].type=1

    def addVWall(self,y,start=0,end=0):
        if not end:
            end=self.columns-1
        row=self[y]
        for i,t in enumerate(row):
            if i in range(start,end) and i!=0 and i!=self.columns-1:
                t.type=2

    def fillArea(self,tl,br,type):
        area=self
        for row in area:
            if row[0].y in range(tl[1],br[1]):
                for t in row:
                    if t.x in range(tl[0],br[0]):
                        if type in TILESET:
                            t.type=type
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
            __str+=__row+'\n'
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
    stage=Matrix(16,35,room=True)
    stage.set(6,4,Tile(type='hero'))
    stage.addVWall(6)
    stage.addVWall(8,end=15)
    stage.addHWall(15)
    stage.set(15,4,Tile(type='door_open_v'))
    stage.set(15,7,Tile(type='door_closed_v'))
    stage.set(3,6,Tile(type='door_closed_h'))
    stage.set(18,6,Tile(type='door_closed_h'))
    stage.set(12,8,Tile(type='door_closed_h'))
    stage.set(0,4,Tile(type='window_v'))
    stage.set(4,0,Tile(type='window_h'))
    rooms=[]
    rooms.append(Room(stage.getList(),(0,0),(15,7),'Your room'))
    rooms.append(Room(stage.getList(),(15,0),(35,7),'Kiro room'))
    rooms.append(Room(stage.getList(),(15,6),(35,16),'Main hall'))
    rooms.append(Room(stage.getList(),(0,8),(15,16),'Hall'))
    stage.rooms=rooms
#    stage.removeArea((2,12),(14,14))
    stage.fillArea((2,12),(14,14),'<span style="color:red;">*</span>')
    stage[4][7].sign='<img src="icons/real_poison.png" width="8">'
    return stage
#    t=stage.get(0,0).get('bottom')
#    for i in xrange(30):
#        t=t.get('left')
#        print t.coords

if __name__ == '__main__':
    main()