# -*- coding: utf-8 -*-
__author__ = 'averrin'
import Image


t_dir='../tilesets/'


class Tileset(dict):
    def __init__(self,dir):
        self.dir=dir
        try:
            old_name=open(t_dir+'.temp/tileset_name').read()
        except:
            old_name=''
        self.signs={
         0:'1_2_0',
         1:'1_0_15',
         2:'1_1_16',
         3:'1_0_14',
         4:'1_5_14',
         5:'1_0_16',
         6:'1_5_16',
         7:'1_3_17',
         8:'1_3_17',
         9:'1_3_14',
         10:'1_1_17',
         11:'1_0_17',
         12:'1_5_17',
         13:'1_3_15',
         14:'1_3_16',
         'none':' ',
         'door_closed_v':'2_2_10',
         'door_open_v':'1_0_18',
         'door_closed_h':'2_2_10',
         'door_open_h':'1_0_18',
         'window_v':'1_1_20',
         'window_h':'1_1_20',
        }
        if dir!=old_name:
            self.load()

    def load(self):
        infile=[t_dir+'%s/%s.bmp' % (self.dir,i) for i in xrange(3)]
        for i,fname in enumerate(infile):
            try:
                im = Image.open(fname)
                xsize,ysize=im.size
                for row in xrange(31):
                    for col in xrange(7):
                        box = ((xsize/8)*col ,(ysize/32)*row, (xsize/8)*(col+1), (ysize/32)*(row+1))
                        region = im.crop(box)
                        region.save(t_dir+'.temp/%d_%d_%d.png' % (i,col,row), "png")
            except Exception,e:
                print e
        try:
            im = Image.open(t_dir+'%s/chars.png'%self.dir)
            xsize,ysize=im.size
            for row in xrange(15):
                for col in xrange(31):
                    box = ((xsize/32)*col ,(ysize/16)*row, (xsize/32)*(col+1), (ysize/16)*(row+1))
                    region = im.crop(box)
                    region.save(t_dir+'.temp/char_%d_%d.png' % (col,row), "png")
            f=open(t_dir+'.temp/tileset_name','w')
            f.write(self.dir)
        except Exception,e:
            print e

    def __getitem__(self, item):
        try:
            return t_dir+'.temp/%s.png' % self.signs[item]
        except:
            return t_dir+'.temp/%s.png' % item

class Layer(object):
    def __init__(self,type,alpha=True,trans=0):
        self.alpha=alpha
        self.type=type
        self.trans=trans

    def __str__(self):
        return self.type

class Tile(object):
    def __init__(self,x=0,y=0,type='none',stage=''):
        self.type=type
        self.stage=stage
        self.x=x
        self.y=y
        self.coords=(x,y)
        self.desc=''
        self.gdesc=''
        self.sign=''
        self.char=''
        self.layers=[]
        self.items=[]
        self.blocked=False

    def chType(self,type,alpha=True):
#        if self.type=='none':
#            self.layers[0]=self.stage.TILESET[type]
#        else:
        if not self.char:
            self.layers.append(Layer(self.stage.TILESET[type],alpha))
        else:
            self.layers.remove(self.layers[-1])
            self.layers.append(Layer(self.stage.TILESET[type],alpha))
            self.layers.append(self.char.sign)
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

    def onCome(self,char):
        if not self.char:
            if not self.blocked:
                return True
            else:
                return False
        else:
            self.char.onTouch()
            return False

    def setChar(self,char=''):
        if char:
            self.char=char
            self.layers.append(char.sign)
            self.onCharEnter(char)
            char.coord=(self.x,self.y)
            char.tile=self
        else:
            self.layers.remove(self.layers[-1])
            self.onCharLeave(self.char)
            self.char=char
#        print 'char added',self.layers, self.items
        self.stage.core.drawTile(self)

    def onCharEnter(self,char):
        self.stage.core.drawTile(self)
    def onCharLeave(self,char):
        self.stage.core.drawTile(self)

    def __str__(self):
        return str(self.layers)

    def info(self):
        layers=''
        for layer in self.layers:
            layers+=str(layer)+','
        return 'Class: %s, Type: %s <br> Char: %s <br>Layers: %s <br>Items: %s, Blocked: %s' % (self.__class__.__name__, self.type, self.char.Name if self.char else '',layers,len(self.items),self.blocked)


    def onLeft(self,char):
        return True

    
class TransTile(Tile):
    def __init__(self,x=0,y=0,type=1,stage=''):
        Tile.__init__(self,x,y,type,stage=stage)
        self.chType(type)

    def onCharEnter(self,char):
        self.char.setTrans(128)
        self.stage.core.drawTile(self)
    def onCharLeave(self,char):
        self.char.setTrans(0)
        self.stage.core.drawTile(self)


class Wall(Tile):
    def __init__(self,x=0,y=0,type='v',stage=''):
        try:
            Tile.__init__(self,x,y,{'h':2,'v':1}[type],stage=stage)
        except:
            Tile.__init__(self,x,y,type,stage=stage)
        self.chType(self.type)

    def onCome(self,char):
        return False

class InternalWall(Tile):
    def __init__(self,x=0,y=0,type='up',id=0,stage=''):
        if type=='up':
            self.type=2
        else:
            self.type=10
        Tile.__init__(self,x,y,self.type,stage=stage)
        self.chType(self.type,False)
        self.id=id

    def onCome(self,char):
        if (self.type==2 and (char.tile.type!=10 or char.tile.id!=self.id)) or (self.type==10 and (char.tile.type!=2 or char.tile.id!=self.id)):
            if not self.blocked:
                return True
            else:
                return False
        else:
            return False



    def onCharEnter(self,char):
        if self.type==2:
            self.char.setTrans(128)
        self.stage.core.drawTile(self)
    def onCharLeave(self,char):
        self.char.setTrans(0)
        self.stage.core.drawTile(self)



class Window(Tile):
    def __init__(self,x=0,y=0,type='v'):
        Tile.__init__(self,x,y,{'h':'window_h','v':'window_v'}[type])
#        self.layers[0]=self.stage.TILESET[self.type]
        self.chType(self.type)

    def onCome(self,char):
        self.stage.core.app['print'](u'Ухты-йопты, окно!')
        if self.type=='v':
            return False
        else:
            return True

class Door(Tile): #TODO: do something for InternalWalls
    def __init__(self,x=0,y=0,type='v',closed=False,locked=False,lock_force=0,stage=''):
        self.closed=closed
        self.locked=locked
        self.d=type
        self.dict={'h':{False:'door_open_h',True:'door_closed_h'},'v':{False:'door_open_v',True:'door_closed_v'}}
        Tile.__init__(self,x,y,self.dict[self.d][closed],stage=stage)
        self.layers.append(Layer(self.stage.TILESET['door_open_h'],False))
        if closed:
            self.chType(self.dict[self.d][self.closed])

    def onCome(self,char):
        if self.d == 'v':
            return self.open()
        else:
            if char.d == 's':
                return self.open()
            else:
                return True
            
    def onLeft(self,char):
        if char.d=='n':
            return self.open()
        else:
            return True

    def open(self):
        if self.closed:
            if not self.locked:
                self.closed=False
                self.chType(self.dict[self.d][self.closed])
            else:
                self.stage.core.app['print'](u'Заперто!')

            self.stage.core.drawTile(self)
            return False
        else:
            self.stage.core.drawTile(self)
            return True

    def onCharLeave(self,char):
        Tile.onCharLeave(self,self.char)
#        self.close() #It fix door bug

    def close(self):
        self.closed=True
        self.chType(self.dict[self.d][self.closed])
        self.stage.core.drawTile(self)



class Stage(list):
    def __init__(self,rows=1,columns=0,room=False):
        self.rows=rows
        self.columns=columns
        self.room=room

    def init(self):
        for i in xrange(self.rows):
            self.append([])
            for c in xrange(self.columns):
                t=Tile(c,i,stage=self)
                t.stage=self
                self[i].append(t)
        if self.room:
            for i,row in enumerate(self):
                if not i or i == self.rows-1:
                    for c,t in enumerate(row):
                        row[c]=Wall(c,i,'h',stage=self)
                        #implement internalwall
                        try:
#                            self[i+1][c].chType(10,False)
                            self.addHWall(i)
                        except:
                            self.addRow()
                            self.addHWall(i)
#                            self[i+1][c].chType(10,False)
                    if not i:
                        row[0].chType(3)
                        row[-1].chType(4)

                    else:
                        row[0].chType(5)
                        row[-1].chType(6)
                        self[i+1][0].chType(11)
                        self[i+1][-1].chType(12)
                else:
                    for ii,t in enumerate(row):
                        if t.type=='none':
                            t.chType(0,False)
                    if i!=self.rows:
                        row[0]=Wall(c,i,'v',stage=self)
                        row[-1]=Wall(c,i,'v',stage=self)

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
            self[len(self)-1].append(Tile(c,len(self)-1,stage=self))

    def addColumn(self):
        for i,row in enumerate(self):
            row.append(Tile(len(row),i,stage=self))

    def addVWall(self,x,start=0,end=0):
        if not end:
            end=self.rows-1
        for i,row in enumerate(self):
            if i in range(start,end) and i!=0 and i!=self.rows-1:
                row[x]=Wall(row[x].x,row[i].y,'v',stage=self)
            elif not i:
                row[x].chType(9)
            elif i==self.rows-1:
                row[x].chType(7)

    def addHWall(self,y,start=0,end=0,id=0):
        if not end:
            end=self.columns-1
        row=self[y]
        for i,t in enumerate(row):
            if i in range(start,end) and i!=0 and i!=self.columns-1:
                self.set(t.x,t.y,InternalWall(type='up',id=id,stage=self))
                self.set(t.x,t.y+1,InternalWall(type='down',id=id,stage=self))
#                self[y+1][i]=InternalWall(t.x,t.y+1,'down')


    def fillArea(self,tl,br,type):
        area=self
        for row in area:
            if row[0].y in range(tl[1],br[1]):
                for t in row:
                    if t.x in range(tl[0],br[0]):
#                        if type in self.stage.TILESET:
                        t.chType(type)
#                        else:
#                            t.sign=type

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

    def addPass(self,x,y):
        _pass=Tile(stage=self)
        _pass.chType(14)
        self.set(x,y,_pass)
        self.set(x,y-1,Wall(type=13,stage=self))
        self.set(x,y+1,TransTile(type=1,stage=self))

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

    def gen(self):
        pass


class Furniture(object): #Grafics artifacts=(
    def __init__(self,height,width,stage=''):
        self.stage=stage
        self.h=height
        self.w=width
        self.list=[]
        for row in xrange(height):
            self.list.append([])
            for col in xrange(width):
                self.list[row].append('')

    def setPart(self,row,col,type):
        self.list[row][col]=Layer(self.stage.TILESET[type],True)

    def setMap(self,map):
        for i,row in enumerate(map):
            for c,col in enumerate(row):
                self.setPart(i,c,col)

    def place(self,stage,x,y):
        self.stage=stage
        for i,row in enumerate(self.list):
            for c,col in enumerate(row):
                stage[y+i][x+c].layers.append(col)



from stages import stages
class World(object):
    def __init__(self,stages,core):
        self.stages=stages
        for stage in self.stages:
            self.stages[stage].TILESET=core.TILESET

    def getStage(self,id):
        stage=self.stages[id]
        return stage.gen()


