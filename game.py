#!/usr/bin/env python

from rpgbase import *
import sys
#import shell
#from magiclib import Cube



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class World(Cube):
	def __init__(self,items):
		super(self.__class__,self).__init__(Shiver)
		self.init_objects(items)
		self.addList(self.dictAttr('name'),'items')
		self.items=self.list('items')
		self.genItem=genItem
	def init_objects(self,items):
		#self.objects=[]
		for obj in items:
			_obj=obj.copy()
			del _obj['class']
			o=obj['class'](**_obj)
			self.add(o)



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#w=World(WORLD_ITEMS)
#print w.items['Coin']
#a=Gem('emerald',price=1)
#a2=Gem('emerald')
#b=Gem('sapphire')
#c=Gem('ruby')
#d=Gem('diamond')

hero=Hero()
gemchest=GemChest()
inv=hero.inventory
#inv=Inventory()
#shop=Shop([c,b],Coin)
inv.addCoins(Coin,5)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def start():
	from avlib import info
	s = ''
	while (s != 'q'):
		sys.stdout.write(':')
		s = raw_input()
		if s!='q':
			try:
				exec(s)
			except:
				print 'Woot?'



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#start()

#print hero.doll.slots.elements
#i=Wearable('helm','Helm','Head')
#ii=Wearable('hood','Helm','Head')
#h=w.items['Weared Helm']
#a=w.items['Old Armor']
#c=w.items['Gray Cloak']
#hero['Mana']=60
#hero['Level']=2

ITEMS=[]
for i in range(150):
	ITEMS.append(genItem(hero))
#inv.give(w.items.values())

#for i in ITEMS:
	#print i.info
"""	if i.__class__==Weapons:
		print i
		inv.give([i,i])
		print i.wear()
		print hero.Damage
		break
		"""
#from random import choice,randint
#for i in range(10):
	#stat=choice(['Level','Strength','Speed','Intelegence','Agility'])
	#hero._setStat(stat,randint(1,5))
	#hero._refresh()
	#hero.levelUp()
	#hero.info()



"""for i in inv.elements:
	if issubclass(i.__class__,Wearable):
		print 'Wear "%s" [%s] in %s' % (i.name,i,i.slot_name)
		i.wear()

"""
#h.wear()
#a.wear()
#c.wear()
#print c.wear()
#print hero.doll.error
#print inv.listAttr('name')
#print 'Hero Defense: %d' % hero.Defense
#print itersubclasses(Wearable)
#print locals()
"""l=locals().copy()
for e in l:
	#print l[e].__class__
	try:
		if issubclass(l[e],Wearable):
			print l[e]
	except:
		pass
	#print l[e].__class__
"""
#print Ring.__class__
#print Armor.__class__


#start()
#print inv.give(ii)
#print dir(ii)
#test(hero.doll.wear,i)
#print hero.doll.slots.elements
#print hero.doll.slots.listAttr('has_item')
#print hero.doll.slots.listBy('has_item',False)
#print hero.doll.slots.itemBy('name',i.slot_name)
#print i.slot_name in hero.doll.slots.list('has_item',False)
#i.wear()
#print ii.wear
#print hero.doll.listAttr('id')
#test(ii.unwear)
#print hero.doll.listAttr('id')

#print gemchest.add([a,b,c,d])
#print inv.give([a,b,d])
#inv.regShop(shop)
#print shop.elements
#inv.give(shop.buy(a))
#print shop.error
#a.sell()
#c.buy()
#test(a.buy)
#print shop.error
#print inv.elements
#print inv.listAttr('price')
#print inv.listAttr('count')
