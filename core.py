# -*- coding: utf-8 -*-
import random
import re
import uuid
from PyQt4.QtGui import *
import json
import world
from world import TILESET
#import game
from rpgbase import *
from PyQt4.QtCore import *

class Core(object):
    def __init__(self,project):
        self.project=project
        self.items=[]
        global core
        core=self


    def onAppInit(self):
        pass


    def onAppReady(self):
        pass


    def onAppShow(self):
        self.stage=world.main()
        self.stage.core=self
        self.app['setText'](self.stage)
#        self.app['echo']('<style>QWidget * {font-size: 18pt; color:blue;}</style>')
        self.app['print']('Welcome to Darkstream World!')
        self.app['print']('<img src="icons/real_poison.png" height="64">')
        self.app['print'](u'С графикой что-то не выходит=( К тому же тормозит, гад=(')
        self.app['print'](u'Пожалуй сначала функционал, а уже потом рюшечки.')
        self.floor=0
        self.app.connect(self.app, SIGNAL('time'), self.stream)
        self.app.connect(self.app, SIGNAL('track'), self.track)
        self.app.connect(self.app, SIGNAL('redraw'), self.app['redraw'])
        self.stream=Stream()
        self.stream.core=self
        self.stream.app=self.app
        self.app.threads_.append(self.stream)
        self.app.statusbar.showMessage(str('wtf?'))
        self.stream.start()
        self.draw(self.stage)
        self.hero=Hero(chset=10)
        self.h=self.stage[4][6]
        self.hero.spawn(self.h)
        kiro=NPC(chset=9)
        kiro.spawn(self.stage[5][12])

    def stream(self,*args):
        self.app['setStatusMessage']('%s at %s' % (self.hero.Name,self.hero.coord))

#    def setStatusMessage(self,msg):
#        print '#',msg

    def m_redraw(self):
        pass
#        self.app.scene.clear()
#        self.draw(self.stage)

    def m_w(self):
        self.m_move('w')

    def m_e(self):
        self.m_move('e')

    def m_n(self):
        self.m_move('n')

    def m_s(self):
        self.m_move('s')

    def draw(self,stage):
        for row in stage:
            row[0].x=0
            for tile in row:
                self.drawTile(tile)
#                    tile.item=self.app['drawText'](str(tile),tile.y*32,tile.x*32)
        self.app.coord=self.app.scene.addText('')

    def drawTile(self,tile):
        try:
            for index,layer in enumerate(tile.layers):
                tile.items.append(self.app['drawImage'](layer,tile.y*32,tile.x*32))
                tile.items[index].tile=tile
                pm=QPixmap(layer)
                if index: #Sword bug still here=(
                    mask=pm.createHeuristicMask()
                    pm.setMask(mask)
                tile.items[index].setPixmap(pm)
                tile.items[index].update()
        except Exception,e:
            print e


    def m_move(self,d):
        self.hero.move(d)


    def m_itemClicked(self,item):
        pass

    def track(self):
        currentPos = QCursor.pos()
        x = currentPos.x()
        y = currentPos.y()
        item=str(self.app.scene.itemAt(x,y).type)
        self.app.coord.setHtml('<span style="color:green">%d,%d -- %s</span>'%(x,y,item))
#        pass

class NPC(Char):
    def __init__(self,chset,*args,**kwargs):
        Char.__init__(self,*args,**kwargs)
        self.coord=(0,0)
        self.signs={
                    's':TILESET['char_%s_2'%chset],
                    'n':TILESET['char_%s_0'%chset],
                    'e':TILESET['char_%s_1'%chset],
                    'w':TILESET['char_%s_3'%chset],
                    }
        self.sign=self.signs['s']

    def spawn(self,tile):
        tile.setChar(self)
        self.tile=tile

    def onTouch(self):
        core.app['print'](u'Иди на хрен, мальчик!')

    def makeAlive(self):
        print 'ololo'

    def move(self,d):
        self.sign=self.signs[d]
        if self.tile.get(d).onCome():
            self.tile.setChar()
            self.tile = self.tile.get(d)
            self.tile.setChar(self)


class Hero(NPC):
    def __init__(self,*args,**kwargs):
        NPC.__init__(self,*args,**kwargs)

import threading, time
class Stream(QThread):
    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs
        self.i=0
        QThread.__init__(self)
        self.Trig=True

    def do(self,*args,**kwargs):
        pass

    def run(self):
#        for n in xrange(2):
#            time.sleep(1)
        while self.Trig:
            for n in xrange(1):
                time.sleep(0.1)
#            self.app.statusbar.showMessage(str(self.i))
#            self.app['setStatusMessage']('chpok')
            self.app.emit(SIGNAL('redraw'))
            self.app.emit(SIGNAL('time'),str(self.i))
            self.i+=1

#            self.app.emit(SIGNAL('track'))
#        while self.Trig:
#            for n in xrange(self.wait_range):
#                if self.Trig:
#                    time.sleep(1)
#            self.do(*self.args,**self.kwargs)