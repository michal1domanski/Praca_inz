import pygame
import math

BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 0, 0)
NIEBIESKI = (0, 0, 255)
PODSWIETL = (0, 255, 0)

class Gra:
	def __init__(self):
		self.grafika = Grafika()
		self.plansza = Plansza()
		self.tura = NIEBIESKI
		self.wybrany_pionek = None
		self.wybrany_mozliwy_ruch = []

	def setup(self):
		self.grafika.setup()

	def update(self, koordynaty): #koordynaty = wspolrzedne pionka
		self.grafika.update(koordynaty, self.plansza)

	def main(self):
		self.setup()

		while True:
			self.zdarzenia()
			self.update(self.wybrany_pionek)

	def zdarzenia(self):
		self.pozycja_myszy = self.grafika.koordynaty_planszy(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		if self.wybrany_pionek != None:
			self.wybrany_mozliwy_ruch = self.plansza.mozliwe_ruchy(self.pozycja_myszy[0], self.pozycja_myszy[1])

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie != None and self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie.kolor == self.tura:
					self.wybrany_pionek = self.pozycja_myszy
				elif self.wybrany_pionek != None and list(self.pozycja_myszy) in self.plansza.mozliwe_ruchy(self.wybrany_pionek[0],self.wybrany_pionek[1]):
					self.plansza.rusz_pionek(self.wybrany_pionek[0], self.wybrany_pionek[1], self.pozycja_myszy[0], self.pozycja_myszy[1])
					self.koniec_tury()

		
	def koniec_tury(self):
		if self.tura == NIEBIESKI:
			self.tura = CZERWONY
		else:
			self.tura = NIEBIESKI
		
		self.wybrany_pionek = None
		self.wybrany_mozliwy_ruch = []
		print("zmiana tury")

class Grafika:
	def __init__(self):

		self.szerokosc = 800
		self.screen = pygame.display.set_mode((self.szerokosc, self.szerokosc))
		self.wielkosc_pola = math.floor(self.szerokosc / 8)
		self.promien_pionka = math.floor(self.wielkosc_pola / 2)

	def setup(self):
		pygame.init()
		pygame.display.set_caption("Warcaby")

	def update(self, koordynaty, plansza):
		self.narysuj_kwadraty(plansza)
		self.narysuj_pionki(plansza)
		if koordynaty != None:
			self.pokaz_ruchy(koordynaty, plansza)

		pygame.display.update()
		
	def narysuj_kwadraty(self, plansza):
		for i in range(8):
			for j in range(8):
				pygame.draw.rect(self.screen, plansza.matrix[i][j].kolor, (i * self.wielkosc_pola, j * self.wielkosc_pola, self.wielkosc_pola, self.wielkosc_pola))

	def narysuj_pionki(self, plansza):
		for i in range(8):
			for j in range(8):
				if plansza.matrix[i][j].zajecie != None:
					pygame.draw.circle(self.screen, plansza.matrix[i][j].zajecie.kolor, self.koordynaty_pola((i,j)), self.promien_pionka)

	def koordynaty_planszy(self, pixel_x, pixel_y):
		return (math.floor(pixel_x / self.wielkosc_pola), math.floor(pixel_y / self.wielkosc_pola))

	def koordynaty_pola(self, koordynaty_planszy):
		return (koordynaty_planszy[0] * self.wielkosc_pola + self.promien_pionka, koordynaty_planszy[1] * self.wielkosc_pola +self.promien_pionka)

	def pokaz_ruchy(self, koordynaty, plansza):
		self.podswietl = [] #self.plansza.mozliwe_ruchy(koordynaty)
		self.mozliwe_ruchy = plansza.mozliwe_ruchy(koordynaty[0], koordynaty[1])
		if plansza.matrix[koordynaty[0]][koordynaty[1]].zajecie.dama == False:
			if plansza.matrix[koordynaty[0]][koordynaty[1]].zajecie.kolor == CZERWONY:
				for i in range(len(self.mozliwe_ruchy)):
					if self.mozliwe_ruchy[i][0] > koordynaty[0]:
						self.podswietl.append(self.mozliwe_ruchy[i])
			elif plansza.matrix[koordynaty[0]][koordynaty[1]].zajecie.kolor == NIEBIESKI:
				for i in range(len(self.mozliwe_ruchy)):
					if self.mozliwe_ruchy[i][0] < koordynaty[0]:
						self.podswietl.append(self.mozliwe_ruchy[i])
		for i in range(len(self.mozliwe_ruchy)):
			pygame.draw.rect(self.screen, PODSWIETL, (self.mozliwe_ruchy[i][0] * self.wielkosc_pola, self.mozliwe_ruchy[i][1] * self.wielkosc_pola, self.wielkosc_pola, self.wielkosc_pola))

class Plansza: 
	def __init__(self):
		self.matrix = self.stworz_plansze()
	
	def stworz_plansze(self):
		matrix = [[None] * 8 for i in range(8)]

		for i in range(8):
			for j in range(8):
				if i % 2 == 0 and j % 2 == 0:
					matrix[i][j] = Pole(CZARNY)
				elif i % 2 == 0 and j % 2 != 0:
					matrix[i][j] = Pole(BIALY)
				elif i % 2 != 0 and j % 2 == 0:
					matrix[i][j] = Pole(BIALY)
				elif i % 2 != 0 and j % 2 != 0:
					matrix[i][j] = Pole(CZARNY)

		for i in range(8):
			for j in range(3):
				if matrix[i][j].kolor == CZARNY:
					matrix[i][j].zajecie = Pionek(CZERWONY)
			for j in range(5,8):
				if matrix[i][j].kolor == CZARNY:
					matrix[i][j].zajecie = Pionek(NIEBIESKI)

		return matrix
	
	def usun_pionek(self, x, y):
		self.matrix[x][y].zajecie = None

	def rusz_pionek(self, start_x, start_y, koniec_x, koniec_y):
		self.matrix[koniec_x][koniec_y].zajecie = self.matrix[start_x][start_y].zajecie
		self.usun_pionek(start_x, start_y)

		self.dama(koniec_x, koniec_y)

	def end_side_tile(self, y):
		if y == 0:
			return 1
		elif y == 7:
			return 2
		else:
			return 0
	
	def end_top_tile(self, x):
		if x == 0:
			return 1
		elif x == 7:
			return 2
		else:
			return 0

	def mozliwe_ruchy(self, x, y):
		possible_moves = []
		if self.matrix[x][y].zajecie != None:
			if self.end_side_tile(y) == 1:
				if self.end_top_tile(x) == 1:
					if self.matrix[x+1][y+1].zajecie == None:
						possible_moves.append([x+1, y+1]) #lewa góra planszy
				elif self.end_top_tile(x) == 2:
					if self.matrix[x-1][y+1].zajecie == None:
						possible_moves.append([x-1, y+1]) #lewy dół planszy
				elif self.end_top_tile(x) == 0: #lewa strona wszystkie moliwości
					if self.matrix[x-1][y+1].zajecie == None and self.matrix[x+1][y+1].zajecie == None:
						possible_moves.append([x-1, y+1])
						possible_moves.append([x+1,y+1])
					elif self.matrix[x-1][y+1].zajecie == None:
						possible_moves.append([x-1,y+1])
					elif self.matrix[x+1][y+1].zajecie == None:
						possible_moves.append([x+1,y+1])
			elif self.end_side_tile(y) == 2:
				if self.end_top_tile(x) == 1:
					if self.matrix[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y-1]) #prawa góra planszy
				elif self.end_top_tile(x) == 2:
					if self.matrix[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1]) #prawy dół planszy
				elif self.end_top_tile(x) == 0: #prawa strona wszystkie moliwości
					if self.matrix[x-1][y-1].zajecie == None and self.matrix[x+1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1])
						possible_moves.append([x+1,y-1])
					elif self.matrix[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1])
					elif self.matrix[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y-1])
			elif self.end_side_tile(y) == 0:
				if self.end_top_tile(x) == 1:
					if self.matrix[x+1][y+1].zajecie == None and self.matrix[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y+1])
						possible_moves.append([x+1,y-1])
					elif self.matrix[x+1][y+1].zajecie == None:
						possible_moves.append([x+1,y+1])
					elif self.matrix[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y-1])
				elif self.end_top_tile(x) == 2:
					if self.matrix[x-1][y+1].zajecie == None and self.matrix[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y+1])
						possible_moves.append([x-1,y-1])
					elif self.matrix[x-1][y+1].zajecie == None:
						possible_moves.append([x-1,y+1])
					elif self.matrix[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1])
				elif self.end_top_tile(x) == 0:
					if self.matrix[x+1][y+1].zajecie == None:
						possible_moves.append([x+1,y+1])
					if self.matrix[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y-1])
					if self.matrix[x-1][y+1].zajecie == None:
						possible_moves.append([x-1,y+1])
					if self.matrix[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1])
		return possible_moves

	def dama(self, x, y):
		if self.matrix[x][y].zajecie != None:
			if (self.matrix[x][y].zajecie.kolor == NIEBIESKI and y == 0) or (self.matrix[x][y].zajecie.kolor == CZERWONY and y == 7):
				self.matrix[x][y].zajecie.dama == True

class Pionek:
	def __init__(self, kolor, dama = False):
		self.kolor = kolor
		self.dama = dama

class Pole:
	def __init__(self, kolor, zajecie = None):
		self.kolor = kolor
		self.zajecie = zajecie

def main():
	game = Gra()
	game.main()

if __name__ == "__main__":
	main()
