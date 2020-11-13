from checkers_bot import Bot
from checkers_pygame import Plansza, Gra

def main():
	plansza = Plansza()
	game = Gra()
	bot = Bot()
	while True:
		bot_move = bot.move(plansza.stworz_plansze())
		game.action()#bot_checker, bot_move)

if __name__ == "__main__":
	main()