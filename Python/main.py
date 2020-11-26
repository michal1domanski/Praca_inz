from checkers_bot import Bot
from checkers_pygame import Plansza, Gra
import pygame
import pygame_menu

CZERWONY = (255, 0, 0)
NIEBIESKI = (0, 0, 255)

def menu():
	pygame.init()
	surface = pygame.display.set_mode((600, 400))
	menu = pygame_menu.Menu(400, 600, "Witamy", theme=pygame_menu.themes.THEME_DARK)
	menu.add_selector("Poziom Trudności : ",[("Easy", 1), ("Medium", 2), ("Hard", 3), ("Champion", 4)], onchange=set_difficulty)
	menu.add_button("Play", start_game)
	menu.add_button("Quit", pygame_menu.events.EXIT)
	menu.mainloop(surface)

def set_difficulty(difficulty, value):
	if value == 1:
		max_depth = 1
	elif value == 2:
		max_depth = 2
	elif value == 3:
		max_depth = 3
	elif value == 4:
		max_depth = 4

def start_game():
	if __name__ == "__main__":
		main(max_depth)

def main(max_depth):
	plansza = Plansza()
	game = Gra()
	bot = Bot(max_depth)
	env = None
	licznik_rund = 1
	print_value = True
	while True:
		bot_move = []
		# if żeby wartości wyświetlały sie raz na turę
		if game.tura == CZERWONY:
			print(f"################ Turn red #{licznik_rund} #####################")
			if licznik_rund == 0:
				bot_move = bot.move(plansza.stworz_plansze(), game.koniec_gry())
			else:
				bot_move = bot.move(env, game.koniec_gry()) 
			licznik_rund += 1	
			print_value = True

		elif game.tura == NIEBIESKI and print_value == True:
			print(f"################ Turn blue #{licznik_rund} #####################")
			print_value = False
			licznik_rund += 1
		
		env = game.action(bot_move)

# aktywacja menu i gry
max_depth = 1
menu()