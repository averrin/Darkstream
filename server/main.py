#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../shared')
from avlib import Project, App, logger, API, loadIcons, getFileContent, cwd
from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *
from datetime import datetime
import os
import re
import time

__author__ = 'averrin'


from sm import SettingsManager

icons=loadIcons('../icons/')

starttime=datetime.now()

#TODO: QDir QDirIterator


class myAPI(API):
    def __init__(self):
        super(myAPI,self).__init__()
        self.logger=logger.name('api')

    def info(self,*args,**kwargs):
        self.ex('info')(*args,**kwargs)

    def debug(self,*args,**kwargs):
        self.ex('debug')(*args,**kwargs)

    def error(self,*args,**kwargs):
        self.ex('error')(*args,**kwargs)

class myLogger(API):
    def __init__(self):
        super(myLogger,self).__init__()
        self.logger=logger.name('api')

    def info(self,*args,**kwargs):
        self.ex('info')(*args,**kwargs)

    def debug(self,*args,**kwargs):
        self.ex('debug')(*args,**kwargs)

    def error(self,*args,**kwargs):
        self.ex('error')(*args,**kwargs)

#TODO: log dockwidget to independent class
#TODO: protect passwords

class Springstone(QMainWindow,App):
    def __init__(self, *args,**kwargs):
        self.threads_=[]
        self.login_window=''
        QMainWindow.__init__(self)
        uic.loadUi(cwd+"main.ui", self)
        self.trayIconPixmap = QIcon(icons['app'])
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIconMenu = QMenu(self)
        App.__init__(self,*args,**kwargs)
        self.connect(self.trayIcon, SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self['toggle'])
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QIcon(self.trayIconPixmap))
        self.resize(QSize(int(self.options['width']),int(self.options['height'])))
        self.setWindowTitle(self.settings['name'])
        self.setWindowIcon(QIcon(icons['app']))
        self.dockWidget.hide()
        self.statusbar.showMessage('Done')
        self.toolBar.setIconSize(QSize(int(self.options['tbicon_size']),int(self.options['tbicon_size'])))
        self.toolBar.setMovable(False)
        self.pb=''
        self.mayhide=eval(self.options['hide'])

        sm=SettingsManager(self)
        sm.setWindowIcon(QIcon(icons['configure']))
        self.appendSM(sm)
#        self.mainList.setAutofillBackground(True)
#        if 'bgcolor' in self.options:
#            self.mainList.setBackground(QColor(self.options['bgcolor']))

        self.connect(self.debugLine, SIGNAL("textChanged(QString)"),self.newchar)
        self.connect(self.debugLine, SIGNAL("returnPressed()"),self.command)

        self.mainList.setIconSize(QSize(int(self.options['mlicon_size']),int(self.options['mlicon_size'])))
#        self.connect(self.mainList, SIGNAL("itemClicked(QListWidgetItem *)"), self.itemClicked)
        self.connect(self.mainList, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.itemDoubleClicked)

        self['info']('Application initialized')

        if eval(self.options['debug']):
            self['addToolButton']('warning','main','toggleDebug')

        self['addToolButton']('ok','main','about')
        self['addToolButton']('help','main','help')
        if eval(self.options['hide']):
            self['addToolButton']('cross','main','exit')
        self['addToMenu']('error','Quit','main','exit')
        self.trayIcon.show()

        self.toolBar.addWidget(QLabel('Search:'))
        self.searchLine=QLineEdit()
        self.toolBar.addWidget(self.searchLine)
        self.connect(self.searchLine, SIGNAL("textChanged(QString)"),self.search)
        self.core.onAppReady()

    def search(self,line):
        result=self.mainList.findItems(line,Qt.MatchContains)
        items = []
        for index in xrange(self.mainList.count()):
            item=self.mainList.item(index)
            if not item.deleted:
                items.append(item)
        for item in items:
            if item not in result:
                self.mainList.setItemHidden(item,True)
            else:
                self.mainList.setItemHidden(item,False)

    def m_createWindow(self,uifile):
        window=QMainWindow()
        uic.loadUi(uifile, window)
        return window

    def m_createLoginWindow(self,uifile):
        window=QMainWindow()
        uic.loadUi(uifile, window)
        self.login_window=window
        window.connect(window.saveButton,SIGNAL('clicked'),self.getLoginInfo)
        return window

    def getLoginInfo(self):
        self.login_window.close()
        self.getAuth()

    def m_addToMenu(self,icon,title,plugin,method):
        a = QAction(self)
        a.setIcon(QIcon(icons[icon]))
        a.setIconText(title)
        self.connect(a, SIGNAL('triggered()'), self.getMethod(plugin,method))
        self.trayIconMenu.addAction(a)


    def m_toggle(self,reason):
        if reason==3:
            if self.isVisible():
                self.hide()
            else:
                self.show()

    def itemClicked(self,item):
        try:
            self.exMethod(item.plugin,'itemClicked',item)
        except:
            self['error']('%s have no itemClicked() method' % (item.plugin))

    def m_removeItem(self,item):
        #FIXME: this
        self.mainList.setItemHidden(item,True)
        item.deleted=True
#        self.mainList.removeChild(item)

    def itemDoubleClicked(self,item):
        try:
            self.exMethod(item.plugin,'itemClicked',item)
        except:
            self['error']('%s have no itemClicked() method' % (item.plugin))

    def m_addListItem(self,*args,**kwargs):
        item=self.makeMessage(*args,**kwargs)
        item.deleted=False
        size=QSize()
        size.setHeight(int(self.options['listitem_height']))
        item.setSizeHint(size)
        self.mainList.addItem(item)
        parent=self.mainList
        widget=QWidget(parent)
        item.widget=widget
        hb=QHBoxLayout(widget)
        widget.setLayout(hb)
        widget.hb=hb
        hb.addSpacerItem(QSpacerItem(int(self.options['width']),0))
        self.mainList.setItemWidget(item,widget)
        widget.show()

        return item


    def my_clickedEvent(self,event):
        print 'boom'
        event.accept()

    def m_addItemButton(self,item,icon,method):
        widget=item.widget
        hb=widget.hb
        bt=QPushButton(QIcon(icons[icon]),'')
        bt.setBaseSize(QSize(int(self.options['mlbt_size']),int(self.options['mlbt_size'])))
        bt.setIconSize(QSize(int(self.options['mlbt_size'])-4,int(self.options['mlbt_size'])-4))
        bt.setFlat(True)
        bt.method=method
        bt.item=item
        bt.clicked.connect(self.sig_map)
        hb.insertWidget(1,bt)

    def sig_map(self):
        try:
            self.sender().method(self.sender().item)
        except:
            self.sender().method()

    def newchar(self):
        ln=re.findall('[^ ]*',str(self.debugLine.text()))[0]
        module=re.findall('([^ ]*)\.',str(self.debugLine.text()))
        if module:
            module=module[0]
            ln=ln.replace(module+'.','')
        if self.getMethod('main',ln):
            self.color = QColor(0, 150, 0)
            self.decor='underline'
            self.dlock=False
        elif self.getMethod(module,ln):
            self.color = QColor(0, 150, 0)
            self.decor='underline'
            self.dlock=False
        else:
            self.color = QColor(140, 0, 0)
            self.decor='none'
            self.dlock=True
#            self.color = QtGui.QColor(30, 144, 255)
        self.debugLine.setStyleSheet("QWidget { font: bold; color: %s; text-decoration: %s;}" % (self.color.name(),self.decor))

    def command(self):
        if not self.dlock:
            line=re.findall('[^ ]*',str(self.debugLine.text()))
            ln=line[0]
            module=re.findall('([^ ]*)\.',str(self.debugLine.text()))
            if module:
                module=module[0]
                ln=ln.replace(module+'.','')
            else:
                module='main'
            args=line[1:]
            for arg in args:
                if not arg:
                    args.remove(arg)
            try:
                self.getMethod(module,ln)(*args)
                self.debugLine.clear()
            except Exception,e:
                self['error'](str(e))
#        self['setStatusMessage'](self.debugLine.text())
#        pass

    def m_toggleDebug(self):
        if self.dockWidget.isHidden():
            self.dockWidget.show()
        else:
            self.dockWidget.hide()


    def keyPressEvent(self, event):
        if event.key()==16777216:
            self.searchLine.clear()

    def appendSM(self,sm):
        self.smTB=QToolButton()
        self.smTB.setIcon(QIcon(icons['configure']))
        self.toolBar.addWidget(self.smTB)
        self.connect(self.smTB, SIGNAL("clicked()"), self.sm.show)

    def m_info(self,msg):
        self.debugList.addItem(self.makeMessage(msg,'lightgreen','ok',ts=True,fgcolor='black'))

    def m_debug(self,msg):
        self.debugList.addItem(self.makeMessage(msg,'lightyellow','warning',ts=True,fgcolor='black'))

    def m_echo(self):
        if self.statusbar.currentMessage():
            self['busy']()
        else:
            self['done']()

    def m_exit(self):
        self.mayhide=False
        QMainWindow.close(self)

    def m_busy(self):
        self.statusbar.clearMessage()
        if not self.pb:
            self.pb=QProgressBar()
        self.pb.setMaximum(0)
        self.pb.setMinimum(0)
        self.statusbar.addWidget(self.pb)
        self.pb.show()

    def m_done(self):
        self.statusbar.removeWidget(self.pb)
        self['setStatusMessage']('Done')


    def m_input(self,title='Input dialog',text='Please input'):
        input=''
        input=QInputDialog.getText(self,title,text)
        self['debug']('input value: %s' % input[0])
        return input[0]

    def m_dialog(self,type='info',title='Dialog',text='oops!!'):
        if type=='info':
            QMessageBox.information(self,title,text)
        elif type=='warning':
            QMessageBox.warning(self,title,text)
        elif type=='critical':
            QMessageBox.critical(self,title,text)
        elif type=='about':
            QMessageBox.about(self,title,text)

    def m_addToolButton(self,icon,plugin,method):
        tb=QToolButton()
        tb.setIcon(QIcon(icons[icon]))
        self.toolBar.addWidget(tb)
        self.connect(tb, SIGNAL("clicked()"), self.getMethod(plugin,method))
        return tb

    def m_addToolSeparator(self):
        self.toolBar.addSeparator()

    def m_setStatusMessage(self,msg):
        self.statusbar.showMessage(msg)

    def makeMessage(self,msg,color='',icon='',bold=True,fgcolor='',ts=False):
        if ts:
            timestamp=datetime.now().strftime('%H:%M:%S')
            item=QListWidgetItem('[%s] %s' % (timestamp,msg))
        else:
            item=QListWidgetItem(msg)
        if 'listitem_bgcolor' in self.options and not color:
            color=self.options['listitem_bgcolor']
        if color:
            item.setBackground(QColor(color))
        if 'listitem_font' in self.options:
            font=QFont(self.options['listitem_font'])
        else:
            font=QFont('Sans')
        font.setBold(bold)
        font.setPointSize(int(self.options['font_size']))
        item.setFont(font)
        if not fgcolor and 'listitem_fgcolor' in self.options:
            fgcolor=self.options['listitem_fgcolor']
        item.setTextColor(QColor(fgcolor))
        if icon:
            item.setIcon(QIcon(icons[icon]))
        return item

    def m_error(self,msg,obj=''):
        if not obj:
            self.debugList.addItem(self.makeMessage(msg,'red','error',ts=True,fgcolor='black'))
        else:
            self.debugList.addItem(self.makeMessage('%s::%s' % (obj,msg),'red','error',ts=True,fgcolor='black'))

    def m_restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv).getErrorMessage()

    def m_about(self):
        self['dialog']('about','About %s' % self.settings['name'],\
                       'Version:    %s<br>Author:   <a href="mailto:%s">%s</a><br>%s' % \
                        (self.settings['version'],self.settings['email'],self.settings['author'],\
                        getFileContent(cwd+'README')))

    def m_help(self):
        self['dialog']('about','Help',getFileContent(cwd+'HELP'))

    def m_addWorker(self,method,*args,**kwargs):
        iw=ItemWorker(*args,**kwargs)
        iw.do=method
        iw.start()
        self.threads_.append(iw)
        self.logapi.debug('New Worker: %s with %s' % (iw,args))
        return iw

    def closeEvent(self,event):
#        if not self.mayhide:
#            try:
#                self.core.reactor.stop()
#            except:
#                pass
#            event.accept()
#        else:
#            event.ignore()
#            self.hide()
        event.accept()
        #TODO: fix exit stack
        self.core.stopServer()



import threading
class ItemWorker(threading.Thread):
    def __init__(self,wait_range,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs
        self.wait_range=wait_range
        threading.Thread.__init__(self)
        self.Trig=True



    def do(self,*args,**kwargs):
        pass

    def run(self):
        while self.Trig:
            for n in xrange(self.wait_range):
                if self.Trig:
                    time.sleep(1)
            self.do(*self.args,**self.kwargs)


def main():
    project=Project()
    logapi=myLogger()
    api=myAPI()
    api.icons=icons
    qtapp = QApplication(sys.argv)
    app=Springstone(project,logapi=logapi,api=api)

    app.show()
    endtime=datetime.now()
    delta=endtime-starttime
    app['debug']('Initialization time: %s' % delta)
    app.core.onAppShow()
    qtapp.exec_()
    for t in app.threads_:
        t.Trig=False


if __name__ == '__main__':
    main()
