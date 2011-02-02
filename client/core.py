# -*- coding: utf-8 -*-
from world import WORLD
from npc import NPCs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import json

class Core(object):
    def __init__(self,project):
        self.project=project
        self.items=[]
        global core
        core=self
        self.clients={}
        self.players={}


    def onAppInit(self):
        pass


    def onAppReady(self):
        pass



    def onError(self,reason):
        self.app['error'](str(reason.getErrorMessage()).decode('utf-8'))

    def m_itemClicked(self,item):
        pass

    def m_send(self,msg):
        self.protocol.sendLine(msg)

    def m_connect(self):
        try:
            self.client.connectTCP("localhost", self.PORT).addCallback(self.client.onConnect).addErrback(self.onError)
            self.online=True
            self.reactor.run()
        except Exception,e:
            self.app['error'](e)

    def m_disconnect(self):
        self.reactor.stop()
        self.api.info("Client disconnected")
        self.status.setText('My\noffline')
        self.status.setIcon(QIcon(self.api.icons['offline']))
        self.online=False

    def m_toggleconnect(self):
        if self.online:
            self.m_disconnect()
        else:
            self.m_connect()




    def onAppShow(self):

        self.status=self.api.exMethod('main','addListItem','Me\noffline',icon='offline')
        self.api.exMethod('main','addItemButton',self.status,'update',self.m_toggleconnect)
        self.status.plugin='main'


        self.api.info("Client init successfully")

        #=====================
        self.stage=WORLD.getStage('FS')
        self.stage.core=self
        self.app['setText'](self.stage)
#        self.app['echo']('<style>QWidget * {font-size: 18pt; color:blue;}</style>')
        self.app['print']('Welcome to Darkstream World!')
        self.app['print']('<img src="../icons/real_poison.png" height="64">')
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


        #==========================

        self.twisted__init__()
        self.client.core=self
        self.m_connect()




    def m_uid(self,uid,*args):
        self.uid=uid
        print 'uid',self.uid
        self.app['debug']('My uid: %s' % uid)

    def m_list(self,*args):
        for friend in args:
            self.m_new(friend)

    def m_new(self,dict,*args):
        friend=dict
        uid=friend['uid']
        if hasattr(self,'uid') and uid!=self.uid and uid not in self.clients:
            print 'new',self.uid,uid
            self.clients[uid]=friend
            self.clients[uid]['status']=self.api.exMethod('main','addListItem','%s\nonline' % friend['name'],icon='online')
            self.api.info("%s online" % friend['name'])
            other=NPCs['other']
            xy=eval(friend['coord'])
            other.spawn(self.stage[xy[1]][xy[0]])
            self.players[uid]=other
#            self['drawTile'](self.stage[6][6])
        elif hasattr(self,'uid') and uid==self.uid:
            pass
        elif hasattr(self,'uid'):
            self.clients[uid]['name']=friend['name']
            self.clients[uid]['status'].setText('%s\nonline' % friend['name'])
            self.api.info("%s know as %s" % (friend['uid'],friend['name']))


    def m_left(self,uid):
        self.api.exMethod('main','removeItem',self.clients[uid]['status'])
        self.api.info("%s offline" % self.clients[uid]['name'])
        self.players[uid].remove()
        del self.clients[uid]


    def twisted__init__(self):

        import qt4reactor

        qt4reactor.install()

        from twisted.internet import reactor
        from twisted.internet.protocol import ServerFactory, ClientCreator
        from twisted.protocols.basic import LineReceiver

        self.PORT=int(self.app.options['port'])
        self.reactor=reactor
        core=self

        class Client(LineReceiver):
            def reg(self):
                nick=core.app.options['nickname']
                self.sendLine('{"sign":"name","args":["%s","%s"]}' % (nick,core.hero.coord))
                core.api.info("Login as %s" % nick)
                core.ci=self

            def move(self):
                self.sendLine('{"sign":"move","args":["%s","%s"]}' % core.hero.coord)


            def init(self):
                self.ready=False

            def dataReceived(self, line):
                if not self.ready:
                    self.ready=True
                    self.reg()
                    core.status.setText('Me\nonline')
                    core.status.setIcon(QIcon(core.api.icons['online']))
                    print 'Greeting: [%s]' % line
                    return ''


                try:
                    line=line.replace('\'','"').replace('\r\n','').replace('u"','"')
                    line=json.loads(line)
                    ln=line['sign']
                    args=line['args']

                    for arg in args:
                        if not arg:
                            args.remove(arg)
                    try:
                        m=core.app.getMethod('main',ln)
                        print ln,m,args
                        m(*args)
                        core.app['debug']('Remote execution: %s (%s)' % (m.func_name,args))
                    except Exception,e:
                        core.app['error'](str(e))
                except Exception,e:
                    print line
                    print e

        self.client = ClientCreator(reactor, Client)

        def onConnect(protocol):
            self.api.info("Client connected successfully")
            protocol.init()
            self.protocol=protocol

        self.client.onConnect=onConnect

        

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
        self.ci.move()

    def m_p_move(self,char):
        xy=eval(char['coord'])
        uid=char['uid']
        char=self.players[uid]
        char.remove()
        char.spawn(self.stage[xy[1]][xy[0]])


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