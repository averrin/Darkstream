# -*- coding: utf-8 -*-
from world import WORLD
from npc import NPCs
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
        self.stage=WORLD.getStage('FS')
        self.stage.core=self
        self.app['setText'](self.stage)
#        self.app['echo']('<style>QWidget * {font-size: 18pt; color:blue;}</style>')
        self.app['print']('Welcome to Darkstream World!')
        self.app['print']('<img src="icons/real_poison.png" height="64">')
        self.app['print'](open('TODO').read().replace('\n','<br>'))
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
        for npc in NPCs:
            NPCs[npc].core=self
        self.hero=NPCs['Hero']
        self.h=self.stage[4][6]
        self.hero.spawn(self.h)
        kiro=NPCs['Kiro']
        kiro.spawn(self.stage[5][12])

    def stream(self,*args):
        self.app['setStatusMessage']('%s at %s' % (self.hero.Name,self.hero.coord))

#    def setStatusMessage(self,msg):
#        print '#',msg

    def m_redraw(self):
        pass
#        self.app['echo']('Hero at %s\nTransparency: %s'%(self.hero.coord,self.hero.sign.trans))
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
            for i,item in enumerate(reversed(tile.items)):
                if i:
                    self.app.scene.removeItem(item)
                tile.items.remove(item)
            for index,layer in enumerate(tile.layers):
                item=self.app['drawImage'](layer,tile.y*32,tile.x*32)
                tile.items.append(item)
                item.tile=tile
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


if __name__ == '__main__':
    core=Core()