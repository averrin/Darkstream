from world import Stage, Door, Room

__author__ = 'averrin'

def setGen(self, method, name='gen'):
    if name is None:
        name = method.func_name
    setattr(self.__class__, name, method)



stages={'FS':Stage(16,30,room=True)}

def genFS(self):
    stage=self
    stage.addHWall(6)
    stage.addHWall(8,end=15,id=1)
    stage.addVWall(15)
    stage[6][15].chType('1_3_14')
    stage.addPass(15,4)
    stage.addPass(15,7)
    stage.set(3,7,Door(type='h'))
    stage.set(18,7,Door(type='h',closed=True))
    stage.set(12,9,Door(type='h',closed=True,locked=True))
    rooms=[]
    rooms.append(Room(stage.getList(),(0,0),(15,7),'Your room'))
    rooms.append(Room(stage.getList(),(15,0),(35,7),'Kiro room'))
    rooms.append(Room(stage.getList(),(15,6),(35,16),'Main hall'))
    rooms.append(Room(stage.getList(),(0,8),(15,16),'Hall'))
    stage.rooms=rooms
    return stage

setGen(stages['FS'],genFS)
