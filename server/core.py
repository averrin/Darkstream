# -*- coding: utf-8 -*-
import re
import uuid
from PyQt4.QtGui import *
import json

class Core(object):
    def __init__(self,project):
        self.project=project
        self.items=[]
        self.clients={}



    def onAppInit(self):
        pass


    def onAppReady(self):
        pass

    def stopServer(self):
        self.factory.sendMessageToAllClients('{"sign":"disconnect","args":[]')
        self.reactor.stop()

    def m_h(self):
#        self.factory.protocol.sendLine("Boom! Just type ':command' and hit enter.")
        pass

    def onAppShow(self):
        self.status=self.api.exMethod('main','addListItem','Nightgleam\noffline',icon='offline')
        self.twisted__init__()

        self.api.info("Starting Server")
        self.factory = self.ChatProtocolFactory()
        for m in dir(self.factory.protocol):
            if m.startswith('m_'):
                self.app.methods.append({'method':eval('self.factory.protocol.%s' % m),'plugin':'main','sign':m.replace('m_','')})


        self.reactor.listenTCP(self.PORT, self.factory)
        self.api.info("Server started successfully")
        self.status.setText('Nightgleam\nonline on port %s' % self.PORT)
        self.status.setIcon(QIcon(self.api.icons['online']))
        self.reactor.run()

        self.status.setText('Nightgleam\noffline')
        self.status.setIcon(QIcon(self.api.icons['offline']))

    def m_stop(self):
        self.reactor.stop()

    def m_itemClicked(self,item):
#        self.api.exMethod('main','q',self.factory.protocol)
        pass


    def twisted__init__(self):
        import qt4reactor

        qt4reactor.install()

        from twisted.internet import reactor
        from twisted.internet.protocol import ServerFactory
        from twisted.protocols.basic import LineReceiver

        self.PORT=2424
        self.reactor=reactor
        core=self

        class Client(object):
            def __init__(self,name):
                self.id=str(uuid.uuid4())
                self.name=name
                self.ip=name

            def onConnect(self):
                self.item=core.api.exMethod('main','addListItem','%s connected\n[%s]' % (self.name,self.id),icon='client')
                self.item.plugin='main'
                core.clients[self.id]=self

            def refresh(self):
                self.item.setText('%s connected\n%s' % (self.name,self.ip))

        class ChatProtocol(LineReceiver):

            name = ""

            def sendLine(self, line):
                self.transport.write(line.encode('utf-8')+"\r\n")

            def getName(self):
                if self.name!="":
                    return self.name
                return self.transport.getPeer().host

            def new(self):
                self.factory.sendMessageToAllClients('{"sign":"new","args":[{"uid":"%s","name":"%s","ip":"%s","coord":"%s"}]}' % (self.client.id,self.client.name,self.client.ip,self.client.coord))

            def m_move(self,x,y):
                self.client.coord=(int(x),int(y))
                self.factory.sendMessageToAllClients('{"sign":"p_move","args":[{"uid":"%s","coord":"%s"}]}' % (self.client.id,self.client.coord))
            def uid(self):
                self.sendLine('{"sign":"uid","args":["%s"]}' % self.client.id)

            def sendList(self):
                cllist=[]
                for client in core.clients:
                    client=core.clients[client]
                    cllist.append({"uid":client.id,"name":client.name,"ip":client.ip,"coord":str(client.coord)})

                self.sendLine('{"sign":"list","args":%s}' % cllist)

            def connectionMade(self):
                core.api.info("New connection from "+self.getName())
                self.client=Client(self.getName())
                self.client.protocol=self
                self.sendLine("Welcome to Nightgleam server.")
                reactor.callLater(1, self.uid)
                reactor.callLater(2, self.new)
                reactor.callLater(3, self.sendList)
                self.factory.clientProtocols.append(self)
                self.client.onConnect()


            def connectionLost(self, reason):
                self.factory.clientProtocols.remove(self)
                core.api.exMethod('main','removeItem',self.client.item)
                self.factory.sendMessageToAllClients('{"sign":"left","args":["%s"]}' % self.client.id)
                del core.clients[self.client.id]

            def lineReceived(self, line):
                core.api.info(self.getName()+" said "+line)
#                line=re.findall('([^ ]*)',line)
                line=json.loads(line)
                ln=line['sign']
                args=line['args']

                for arg in args:
                    if not arg:
                        args.remove(arg)
                try:
                    m=core.app.getMethod('main',ln)
                    try:
                        m(*args)
                    except:
                        m(self,*args)
                    core.app['debug']('Remote execution: %s (%s)' % (m.func_name,args))
                except Exception,e:
                    core.app['error'](str(e))
                    self.sendLine("Wrong command.")


            def m_name(self,name,coord):
                self.name = name
                self.client.name = name
                self.client.coord=coord
                self.client.refresh()
                self.new()

            def m_q(self):
                self.transport.loseConnection()
                self.factory.sendMessageToAllClients('{"sign":"left","args":["%s"]}' % self.client.id)

        class ChatProtocolFactory(ServerFactory):

            protocol = ChatProtocol

            def __init__(self):
                self.clientProtocols = []

            def sendMessageToAllClients(self, mesg):
                for client in self.clientProtocols:
                    client.sendLine(mesg)

        self.ChatProtocol=ChatProtocol
        self.ChatProtocolFactory=ChatProtocolFactory



