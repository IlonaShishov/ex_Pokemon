
import time
import json
import random

from ability import Ability

with open('project.json') as file:
	database = json.load(file)

pokemon_db = database["POKEMON"]
abilities_db = database["ABILITIES"]

abilities_dict = {}
for tp in abilities_db.values():
	for atk, dtls in tp.items():
		abilities_dict[atk] = Ability(*dtls)

class Pokemon:
	"""docstring for Pokemon"""
	def __init__(self, name, pokemon, level=1):
		try:
			if pokemon.upper() not in pokemon_db:
				raise Exception("That\'s not a valid pokemon!")
			self.name = name
			self.level = level
			self.pokemon = pokemon.upper()
			self.originalPoke = pokemon.upper()
			self.type = pokemon_db[pokemon.upper()]['TYPE']
			self.abilities = [*abilities_db['GENERAL'].keys(), *abilities_db[self.type].keys()]
			self.hp = 100 
			self.xp = 0
		except Exception as inst:
			return inst

	def level_up(self):
		self.level += 1
		print(f'Level Up!!! {self.name} is now level *{self.level}*')
		self.hp += 50
		self.xp = 0
		if (str(self.level) in pokemon_db[self.originalPoke]["EVOLUTIONS"]):
			self.pokemon = pokemon_db[self.originalPoke]["EVOLUTIONS"][str(self.level)]
			print(f'Wait! {self.name} is evolving!!!', end = " ")
			for dot in "...":
				print(dot, end = " "),
				time.sleep(.7)
			print(f'{self.name} evolved into {self.pokemon}!!!')

	def attack(self, target, ability):
		try:
			if ability.upper() not in abilities_dict:
				raise Exception("That\'s not a valid ability!")
			elif not isinstance(target, Pokemon):
				raise Exception("Can\'t attack that")
			else: 
				atk = abilities_dict[ability.upper()]
				if (random.uniform(0, 1) > atk.precision):
					print(f'{self.name} attacks {target.name} with {atk.name}.... attack missed')
				else:
					print('*BOOM* '*6)
					print(f'{self.name} attacks {target.name} with {atk.name}.... {target.name} recieved {atk.damage}hp damage')
					fainted = target.receive_damage(atk.damage)
					if fainted:
						self.victory()
		except Exception as inst:
			return inst

	def receive_damage(self, damage):
		self.hp -= damage
		if self.hp <= 0:
			self.hp = 0
			self.faint()
			return True
		return False

	def faint(self):
		print(f'{self.name} has fainted!')

	def victory(self):
		self.xp += 50
		if self.xp == (50 + self.level * 50):
			self.level_up()

	def get_pokemon():
		return list(pokemon_db.keys())
