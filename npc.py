# -*- coding: utf-8 -*-
from rpgbase import Char
from world import Layer,TILESET

__author__ = 'averrin'

class NPC(Char):
    def __init__(self,chset,*args,**kwargs):
        Char.__init__(self,*args,**kwargs)
        self.coord=(0,0)
        self.signs={
                    's':Layer(TILESET['char_%s_2'%chset]),
                    'n':Layer(TILESET['char_%s_0'%chset]),
                    'e':Layer(TILESET['char_%s_1'%chset]),
                    'w':Layer(TILESET['char_%s_3'%chset]),
                    }
        self.sign=self.signs['s']

    def setTrans(self,trans):
        for layer in self.signs:
            self.signs[layer].trans=trans

    def spawn(self,tile):
        tile.setChar(self)
        self.tile=tile

    def onTouch(self):
        self.core.app['print'](u'Иди на хрен, мальчик!')

    def makeAlive(self):
        print 'ololo'

    def move(self,d):
        self.sign=self.signs[d]
        if self.tile.get(d).onCome(self):
            self.tile.setChar()
            self.tile = self.tile.get(d)
            self.tile.setChar(self)


class Hero(NPC):
    def __init__(self,*args,**kwargs):
        NPC.__init__(self,*args,**kwargs)
def genHero():
    hero=Hero(chset=10)
    return hero


NPCs={'Kiro':NPC(chset=9),'Hero':genHero()}

#if __name__ == '__main__':
#    core=Core()