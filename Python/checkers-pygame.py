import pygame
import math
import sys
'''
ZASADY
-pozniej sobie to napisze. narazie mi sie nie chce.
'''

BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 0, 0)
NIEBIESKI = (0, 0, 255)
PODSWIETL = (0, 255, 0)
NIEBIESKA_DAMA = (0, 255, 255)
CZERWONA_DAMA = (255, 255, 0)

class Gra:
	def __init__(self):
		self.grafika = Grafika()
		self.plansza = Plansza()
		self.tura = NIEBIESKI
		self.tura_dama = NIEBIESKA_DAMA
		self.wybrany_pionek = None
		self.bijace_pionki = []
		self.wybrany_mozliwy_ruch = []
		self.bicie = False
		self.bicie_macierz = []

	def setup(self):
		self.grafika.setup()

	def update(self, koordynaty): #koordynaty = wspolrzedne pionka
		self.grafika.update(koordynaty, self.plansza)

	def main(self):
		self.setup()

		while True:
			self.akcje()
			self.koniec_gry()
			self.zdarzenia()
			self.update(self.wybrany_pionek)
			
	def zdarzenia(self):
		self.pozycja_myszy = self.grafika.koordynaty_planszy(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		if self.wybrany_pionek != None:
			self.wybrany_mozliwy_ruch = self.plansza.mozliwe_ruchy(self.pozycja_myszy[0], self.pozycja_myszy[1])
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.bicie == False:
					
					for i in range(8):
						for j in range(8):
							if hasattr(self.plansza.matrix[i][j].zajecie, "kolor") == True:
								if self.plansza.matrix[i][j].zajecie.kolor == self.tura or self.plansza.matrix[i][j].zajecie.kolor == self.tura_dama:
									if self.plansza.bicie(i,j) != []:
										self.bicie = True
										self.bijace_pionki.append([i,j])
										break

					if self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie != None and (self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie.kolor == self.tura or self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie.kolor == self.tura_dama):

						self.wybrany_pionek = self.pozycja_myszy
						self.bicie_macierz = self.plansza.bicie(self.pozycja_myszy[0], self.pozycja_myszy[1])

					elif self.wybrany_pionek != None and list(self.pozycja_myszy) in self.plansza.mozliwe_ruchy(self.wybrany_pionek[0],self.wybrany_pionek[1]):

						if (self.wybrany_pionek[1] > self.pozycja_myszy[1] and self.plansza.matrix[self.wybrany_pionek[0]][self.wybrany_pionek[1]].zajecie.kolor == NIEBIESKI) or (self.wybrany_pionek[1] < self.pozycja_myszy[1] and self.plansza.matrix[self.wybrany_pionek[0]][self.wybrany_pionek[1]].zajecie.kolor == CZERWONY): #określenie kierunku poruszania się

							self.plansza.rusz_pionek(self.wybrany_pionek[0], self.wybrany_pionek[1], self.pozycja_myszy[0], self.pozycja_myszy[1])
							self.koniec_tury()
					
					if self.wybrany_pionek != None and self.plansza.matrix[self.wybrany_pionek[0]][self.wybrany_pionek[1]].zajecie.dama == True and list(self.pozycja_myszy) in self.plansza.ukosne(self.wybrany_pionek[0], self.wybrany_pionek[1]):

						self.plansza.rusz_pionek(self.wybrany_pionek[0], self.wybrany_pionek[1], self.pozycja_myszy[0], self.pozycja_myszy[1])
						self.koniec_tury()

				if self.bicie == True:

					if self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie != None and (self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie.kolor == self.tura or self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie.kolor == self.tura_dama):
						self.wybrany_pionek = self.pozycja_myszy

					if self.wybrany_pionek != None and list(self.pozycja_myszy) in self.plansza.bicie(self.wybrany_pionek[0], self.wybrany_pionek[1]):
						self.plansza.rusz_pionek(self.wybrany_pionek[0], self.wybrany_pionek[1],self.pozycja_myszy[0], self.pozycja_myszy[1])

						if self.plansza.matrix[self.pozycja_myszy[0]][self.pozycja_myszy[1]].zajecie.dama == False:
							self.plansza.usun_pionek(math.floor((self.wybrany_pionek[0] + self.pozycja_myszy[0])/2), math.floor((self.wybrany_pionek[1] + self.pozycja_myszy[1])/2))

						else:
							pomoc = [self.wybrany_pionek[0] - self.pozycja_myszy[0], self.wybrany_pionek[1] - self.pozycja_myszy[1]]
							kierunek_usuniecia = [math.floor(pomoc[0]/abs(pomoc[0])), math.floor(pomoc[1]/abs(pomoc[1]))]
							self.plansza.usun_pionek(self.pozycja_myszy[0] + kierunek_usuniecia[0], self.pozycja_myszy[1] + kierunek_usuniecia[1])
						if self.plansza.bicie(self.pozycja_myszy[0], self.pozycja_myszy[1]) == []:
							self.koniec_tury()

						else:
							self.wybrany_pionek = self.pozycja_myszy

	def koniec_tury(self):
		self.plansza.dama(self.pozycja_myszy[0], self.pozycja_myszy[1])

		if self.tura == NIEBIESKI:
			self.tura = CZERWONY
			self.tura_dama = CZERWONA_DAMA
		else:
			self.tura = NIEBIESKI
			self.tura_dama = NIEBIESKA_DAMA		

		self.wybrany_pionek = None
		self.wybrany_mozliwy_ruch = []
		self.bicie = False
		self.bicie_macierz = []

	def koniec_gry(self):
		dostepne_ruchy = []
		pionki_ruchy = []
		for i in range(8):
			for j in range(8):
				if hasattr(self.plansza.matrix[i][j].zajecie, "kolor"):
					if self.grafika.pokaz_ruchy([i, j], self.plansza) != [] and (self.plansza.matrix[i][j].zajecie.kolor == self.tura or self.plansza.matrix[i][j].zajecie.kolor == self.tura_dama):
						dostepne_ruchy.append([self.grafika.pokaz_ruchy([i, j], self.plansza)])
						pionki_ruchy.append([i,j])
		
		if self.tura == NIEBIESKI:
			kolor = "Czerwony"
		else:
			kolor = "Niebieski"

		if dostepne_ruchy == []:
			self.grafika.rysuj_okno("{} gracz wygrywa".format(kolor))
		else:
			return dostepne_ruchy, pionki_ruchy #wszystkie moliwe ruchy - actions do reinforcement learning

	def akcje(self): #do AI
		ruchy, ruchy_bez_bicia = self.koniec_gry()
		bicia = []
		pionki = []
		for x in range(8):
			for y in range(8):
				if hasattr(self.plansza.matrix[x][y].zajecie, "kolor") == True:
					if self.plansza.bicie(x,y) != [] and (self.plansza.matrix[x][y].zajecie.kolor == self.tura or self.plansza.matrix[x][y].zajecie.kolor == self.tura_dama):
						bicia.append(self.plansza.bicie(x,y))
						pionki.append([x,y])
		if bicia == []:
			print(ruchy_bez_bicia)
			return ruchy
		else:
			print(pionki)
			return bicia

class Grafika:
	def __init__(self):

		self.szerokosc = 800
		self.screen = pygame.display.set_mode((self.szerokosc, self.szerokosc))
		self.wielkosc_pola = math.floor(self.szerokosc / 8)
		self.promien_pionka = math.floor(self.wielkosc_pola / 2)
		self.informacja = False

	def setup(self):
		pygame.init()
		pygame.display.set_caption("Warcaby")

	def update(self, koordynaty, plansza):
		self.narysuj_kwadraty(plansza)
		self.narysuj_pionki(plansza)
		if koordynaty != None:
			self.pokaz_ruchy(koordynaty, plansza)

		if self.informacja:
			self.screen.blit(self.napis, self.napis_pole)

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
		self.podswietl = [] 
		self.mozliwe_ruchy = plansza.mozliwe_ruchy(koordynaty[0], koordynaty[1])
		if plansza.bicie(koordynaty[0], koordynaty[1]) == []:
			if plansza.matrix[koordynaty[0]][koordynaty[1]].zajecie.dama == False:
				if plansza.matrix[koordynaty[0]][koordynaty[1]].zajecie.kolor == CZERWONY:
					for i in range(len(self.mozliwe_ruchy)):
						if self.mozliwe_ruchy[i][1] > koordynaty[1]:
							self.podswietl.append(self.mozliwe_ruchy[i])
				elif plansza.matrix[koordynaty[0]][koordynaty[1]].zajecie.kolor == NIEBIESKI:
					for i in range(len(self.mozliwe_ruchy)):
						if self.mozliwe_ruchy[i][1] < koordynaty[1]:
							self.podswietl.append(self.mozliwe_ruchy[i])
			else:
				self.podswietl = plansza.ukosne(koordynaty[0], koordynaty[1])
		else:
			self.podswietl = plansza.bicie(koordynaty[0], koordynaty[1])
		for i in range(len(self.podswietl)):
			pygame.draw.rect(self.screen, PODSWIETL, (self.podswietl[i][0] * self.wielkosc_pola, self.podswietl[i][1] * self.wielkosc_pola, self.wielkosc_pola, self.wielkosc_pola))
		return self.podswietl

	def rysuj_okno(self, info):
		self.informacja = True
		self.czcionka = pygame.font.SysFont("comicsansms", 40)
		self.napis = self.czcionka.render(info, True, PODSWIETL, CZARNY)
		self.napis_pole = self.napis.get_rect()
		self.napis_pole.center = (self.szerokosc/2, self.szerokosc/2) 

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

	def ukosne(self, x, y):
		ruchy = self.mozliwe_ruchy(x, y)
		mozliwe_ruchy_damy = []
		kierunek = []
		for i in range(len(ruchy)):
			kierunek.append([- (x - ruchy[i][0]), - (y - ruchy[i][1])])
			while (ruchy[i][0] >= 0 and ruchy[i][0] <= 7 and ruchy[i][1] >= 0 and ruchy[i][1] <= 7): 
				if self.matrix[ruchy[i][0]][ruchy[i][1]].zajecie == None:
					mozliwe_ruchy_damy.append([ruchy[i][0], ruchy[i][1]])
					ruchy[i][0] += kierunek[i][0]
					ruchy[i][1] += kierunek[i][1]
				else:
					ruchy[i] = [9,9]
		return mozliwe_ruchy_damy
		
	def dama(self, x, y):
		if self.matrix[x][y].zajecie != None:
			if (self.matrix[x][y].zajecie.kolor == NIEBIESKI and y == 0):
				self.matrix[x][y].zajecie.dama = True
				self.matrix[x][y].zajecie.kolor = NIEBIESKA_DAMA
			elif (self.matrix[x][y].zajecie.kolor == CZERWONY and y == 7):
				self.matrix[x][y].zajecie.dama = True
				self.matrix[x][y].zajecie.kolor = CZERWONA_DAMA

	def bicie(self, x, y):
		self.gracz = self.matrix[x][y].zajecie.kolor
		if self.gracz == NIEBIESKI:
			self.damka = NIEBIESKA_DAMA
		elif self.gracz == CZERWONY:
			self.damka = CZERWONA_DAMA
		elif self.gracz == NIEBIESKA_DAMA:
			self.gracz = NIEBIESKI
			self.damka = NIEBIESKA_DAMA
		elif self.gracz == CZERWONA_DAMA:
			self.gracz = CZERWONY
			self.damka = CZERWONA_DAMA

		self.mozliwe_bicie = []
		if self.matrix[x][y].zajecie.dama == False:
			for i in range(len(self.pola_obok(x,y))):
				if hasattr(self.matrix[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie, "kolor") == True:
					if self.matrix[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie.kolor != self.gracz and self.matrix[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie.kolor != self.damka:
						self.wrog = [self.pola_obok(x,y)[i][0],self.pola_obok(x,y)[i][1]]
						self.linia = [(x - self.wrog[0])*2, (y - self.wrog[1])*2]
						self.ruch_bicia = [x - self.linia[0], y - self.linia[1]]
						if (self.ruch_bicia[0] <= 7 and self.ruch_bicia[0] >= 0) and (self.ruch_bicia[1] <= 7 and self.ruch_bicia[1] >= 0):
							if self.matrix[self.ruch_bicia[0]][self.ruch_bicia[1]].zajecie == None:
								self.mozliwe_bicie.append([x-self.linia[0], y-self.linia[1]])
		else:
			pola_dostepne = self.ukosne(x, y)
			for i in range(len(pola_dostepne)):
				odleglosc = [pola_dostepne[i][0] - x, pola_dostepne[i][1] - y]
				kierunek_ruchu = [math.floor(odleglosc[0]/abs(odleglosc[0])), math.floor(odleglosc[1]/abs(odleglosc[1]))]
				pole_wrogiego_pionka = [pola_dostepne[i][0] + kierunek_ruchu[0], pola_dostepne[i][1] + kierunek_ruchu[1]]
				pole_po_biciu = [pole_wrogiego_pionka[0] + kierunek_ruchu[0], pole_wrogiego_pionka[1] + kierunek_ruchu[1]]
				if pole_po_biciu[0] <=7 and pole_po_biciu[0] >= 0 and pole_po_biciu[1] <= 7 and pole_po_biciu[1] >=0:
					if pole_wrogiego_pionka[0] <=7 and pole_wrogiego_pionka[0] >= 0 and pole_wrogiego_pionka[1] <= 7 and pole_wrogiego_pionka[1] >=0:
						if self.matrix[pole_wrogiego_pionka[0]][pole_wrogiego_pionka[1]].zajecie != None and self.matrix[pole_po_biciu[0]][pole_po_biciu[1]].zajecie == None:
							if self.matrix[pole_wrogiego_pionka[0]][pole_wrogiego_pionka[1]].zajecie.kolor != self.gracz and self.matrix[pole_wrogiego_pionka[0]][pole_wrogiego_pionka[1]].zajecie.kolor != self.damka:
								self.mozliwe_bicie.append([pole_po_biciu[0], pole_po_biciu[1]])
				
			for i in range(len(self.pola_obok(x,y))):
				if hasattr(self.matrix[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie, "kolor") == True:
					if self.matrix[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie.kolor != self.gracz and self.matrix[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie.kolor != self.damka:
						self.wrog = [self.pola_obok(x,y)[i][0],self.pola_obok(x,y)[i][1]]
						self.linia = [(x - self.wrog[0])*2, (y - self.wrog[1])*2]
						self.ruch_bicia = [x - self.linia[0], y - self.linia[1]]
						if (self.ruch_bicia[0] <= 7 and self.ruch_bicia[0] >= 0) and (self.ruch_bicia[1] <= 7 and self.ruch_bicia[1] >= 0):
							if self.matrix[self.ruch_bicia[0]][self.ruch_bicia[1]].zajecie == None:
								self.mozliwe_bicie.append([x-self.linia[0], y-self.linia[1]])
		return self.mozliwe_bicie

	def pola_obok(self, x, y):
		pola = []
		if self.end_side_tile(y) == 1: #góra
			if self.end_top_tile(x) == 1: #lewo
				pola.append([x+1, y+1])
			elif self.end_top_tile(x) == 0: #środek
				pola.append([x+1, y+1])
				pola.append([x-1, y+1])
		elif self.end_side_tile(y) == 2: #dół
			if self.end_top_tile(x) == 2: #prawo
				pola.append([x-1, y-1])				
			elif self.end_top_tile(x) == 0: #środek
				pola.append([x+1, y-1])
				pola.append([x-1, y-1])
		elif self.end_side_tile(y) == 0: #środek
			if self.end_top_tile(x) == 1:#lewo
				pola.append([x+1, y+1])
				pola.append([x+1, y-1])
			elif self.end_top_tile(x) == 2:#prawo
				pola.append([x-1, y+1])
				pola.append([x-1, y-1])
			elif self.end_top_tile(x) == 0: #środek
				pola.append([x-1, y+1])
				pola.append([x-1, y-1])
				pola.append([x+1, y+1])
				pola.append([x+1, y-1])
		return pola

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
