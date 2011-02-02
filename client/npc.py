# -*- coding: utf-8 -*-

import sys
sys.path.append('../shared')
from rpgbase import Char
from world import Layer

__author__ = 'averrin'

class NPC(Char):
    def __init__(self,chset,core,*args,**kwargs):
        Char.__init__(self,*args,**kwargs)
        self.coord=(0,0)
        self.core=core
        self.signs={
                    's':Layer(self.core.TILESET['char_%s_2'%chset]),
                    'n':Layer(self.core.TILESET['char_%s_0'%chset]),
                    'e':Layer(self.core.TILESET['char_%s_1'%chset]),
                    'w':Layer(self.core.TILESET['char_%s_3'%chset]),
                    }
        self.sign=self.signs['s']

    def setTrans(self,trans):
        for layer in self.signs:
            self.signs[layer].trans=trans

    def spawn(self,tile):
        tile.setChar(self)
        self.tile=tile

    def remove(self):
        self.tile.setChar()

    def onTouch(self):
        self.core.app['print'](u'Иди на хрен, мальчик!')

    def makeAlive(self):
        print 'ololo'

    def move(self,d):
        self.d=d
        self.sign=self.signs[d]
        if self.tile.onLeft(self) and self.tile.get(d).onCome(self):
            self.tile.setChar()
            self.tile = self.tile.get(d)
            self.tile.setChar(self)


class Hero(NPC):
    def __init__(self,*args,**kwargs):
        NPC.__init__(self,*args,**kwargs)
def genHero(core):
    hero=Hero(10,core)
    return hero


class NPCs(dict):
    def __init__(self,core):
        self.update({'Kiro':NPC(9,core),'Hero':genHero(core),'other':NPC(6,core)})

#if __name__ == '__main__':
#    core=Core()