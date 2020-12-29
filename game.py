import time, random, os, sys, msvcrt

from player import Player
from pokemon import Pokemon

def print_slow(string):
    for letter in string:
        print(letter, end=""),
        sys.stdout.flush()
        time.sleep(.05)

def border(inner_func):
	def bordered_func():
		print(f'\n\n<{"-"*60}>\n\n')
		inner_func()
		print(f'\n\n<{"-"*60}>\n\n')
	return bordered_func

def clear():
	if os.name == 'posix':
		os.system('clear')
	else:
		os.system('cls')

def wait_continue(inner_func):
	timeout = 10
	startTime = time.time()
	inner_func()
	print('%spress any key to continue or wait a few seconds... ' %("\n"*5))
	while True:
		if msvcrt.kbhit():
			if msvcrt.getch() == b'\r':
				break
		elif time.time() - startTime > timeout:
			break
	clear()


clear() #clear screen as start game

#start game message
@wait_continue
@border
def welcome_message():
	print_slow("Welcome to Pokemon!\n")

#ask for players name
print_slow("What is your name?: ")
myplayer = Player(input())

# welcome player to the game
@wait_continue
def welcome_player():
	print_slow(f'\n\nHello {myplayer.name}, welcome to the Game!\n')

# print list of pokemon
pokemon_lst = Pokemon.get_pokemon()
for idx, poke in enumerate(pokemon_lst):
	print_slow(f'{idx+1} - {poke}\n')

# ask player to choose a pokemon and nickname
print_slow("\nChoose your pokemon: ")
mypokemon_type = pokemon_lst[int(input())-1]
print_slow("\nGive it a nickname: ")
mypokemon_name = input()
mypokemon = Pokemon(mypokemon_name, mypokemon_type)

# Welcome new pokemon to the game
@wait_continue
def welcome_pokemon():
	print_slow(f'\n\nGreat! {mypokemon.name} the {mypokemon.pokemon} is ready to go!\n')

# continue while player enters 'y' to continue fighting pokemon
cont = 'y'
while(mypokemon.hp>0 and cont == 'y'):

	# generate random pokemon from db
	rand_pokemon = pokemon_lst[random.randint(0, len(pokemon_lst)-1)]
	wild_pokemon = Pokemon(rand_pokemon, rand_pokemon)
	
	# welcome new wild pokemon to the game
	@wait_continue
	def new_wild_pokemon():
		times = range(0,random.randint(1,5))
		for rep in times:
			for dot in "...":
				print(dot, end = " ")
				sys.stdout.flush()
				time.sleep(.7)
			clear()
		print_slow(f'A WILD *{wild_pokemon.pokemon}* APPEARED!\n\n')
	
	# continue fight while neither pokemon has fainted
	while(mypokemon.hp>0 and wild_pokemon.hp>0):

		# choose attack
		print_slow('What will you do?: \n')
		for idx, ability in enumerate(mypokemon.abilities):
			print_slow(f'{idx+1} - {ability}\n')

		print_slow("\nChoose an attack: ")
		atk = mypokemon.abilities[int(input())-1]
		print('\n')
		clear()

		# Execute attack
		@wait_continue
		def atk_wild_pokemon():
			ex =  Pokemon.attack(mypokemon,wild_pokemon,atk)

		#if wild pokemon faints, end fight
		if wild_pokemon.hp==0:
			break

		# select random ability for wild pokemon to attack
		atk = wild_pokemon.abilities[random.randint(0, len(wild_pokemon.abilities)-1)]
		print_slow(f'{wild_pokemon.pokemon} is angry!\n')

		# Execute attack
		@wait_continue
		def atk_player_pokemon():
			ex =  Pokemon.attack(wild_pokemon,mypokemon,atk)

	# if player did not faint, ask if wishes to continue fighting, otherwise stop game
	if mypokemon.hp>0: 

		print_slow('GREAT JOB! you won!\nWould you like to continue? (y/n): ')
		cont = input()
		clear()
	else: 
		break

print_slow('see you next time!') if mypokemon.hp>0 else print('GAME OVER :( :( :(')