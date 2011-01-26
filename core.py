# -*- coding: utf-8 -*-
import re
import uuid
from PyQt4.QtGui import *
import json
import world
import game

class Core(object):
    def __init__(self,project):
        self.project=project
        self.items=[]


    def onAppInit(self):
        pass


    def onAppReady(self):
        pass


    def onAppShow(self):
        self.app['setText'](world.main())
#        self.app['echo']('<style>QWidget * {font-size: 18pt; color:blue;}</style>')
        self.app['echo']('Welcome to Darkstream World!')
        self.app['echo']('<img src="icons/real_poison.png" height="64">')

    def m_itemClicked(self,item):
        pass

