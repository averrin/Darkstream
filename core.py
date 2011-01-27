# -*- coding: utf-8 -*-
import re
import uuid
from PyQt4.QtGui import *
import json
import world
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
        self.app['setText'](self.stage)
#        self.app['echo']('<style>QWidget * {font-size: 18pt; color:blue;}</style>')
        self.app['print']('Welcome to Darkstream World!')
        self.app['print']('<img src="icons/real_poison.png" height="64">')
        self.app['print'](u'Бумка!')
        self.floor=0
        self.app.connect(self.app, SIGNAL('time'), self.stream)
        self.app.connect(self.app, SIGNAL('redraw'), self.app['redraw'])
        self.stream=Stream()
        self.stream.core=self
        self.stream.app=self.app
        self.app.threads_.append(self.stream)
        self.app.statusbar.showMessage(str('wtf?'))
        self.stream.start()
        self.hero=Hero()
        self.h=self.stage[4][6]
        self.hero.spawn(self.h)
        kiro=NPC()
        kiro.spawn(self.stage[5][12])

    def stream(self,*args):
        self.app['setStatusMessage']('%s at %s' % (self.hero.Name,self.hero.coord))

#    def setStatusMessage(self,msg):
#        print '#',msg

    def m_redraw(self):
        self.app['setText'](self.stage)

    def m_w(self):
        self.m_move('w')

    def m_e(self):
        self.m_move('e')

    def m_n(self):
        self.m_move('n')

    def m_s(self):
        self.m_move('s')


    def m_move(self,d):
        if self.h.get(d).onCome():
#            self.m_redraw()
#            self.h.type=self.floor
            self.h.setChar()
            self.h = self.h.get(d)
#            self.floor=self.h.type
            self.h.setChar(self.hero)
#            self.m_redraw()
#        else:
#            self.m_redraw()

    def m_itemClicked(self,item):
        pass

class NPC(Char):
    def __init__(self,*args,**kwargs):
       Char.__init__(self,*args,**kwargs)
       self.coord=(0,0)
       self.sign='<span style="color:yellow;">◐</span>'

    def spawn(self,tile):
        tile.setChar(self)

    def onTouch(self):
        core.app['print'](u'Иди на хрен, мальчик!')


class Hero(NPC):
    def __init__(self,*args,**kwargs):
        NPC.__init__(self,*args,**kwargs)
        self.sign='<span style="color:green;">◐</span>'

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
#        while self.Trig:
#            for n in xrange(self.wait_range):
#                if self.Trig:
#                    time.sleep(1)
#            self.do(*self.args,**self.kwargs)