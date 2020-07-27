import pygame

CZARNY = (255, 255, 255)
BIALY = (0, 0, 0)
CZERWONY = (255, 0, 0)
NIEBIESKI = (0, 0, 255)

class Gra:
	def __init__(self):
		pass

class Grafika:
	def __init__(self):
		pass

class Plansza: #wydaje mi się e wszystko co potrzebne jest juz napisane w tej czesci
	def __init__(self):
		self.matrix = self.stworz_plansze()
	
	def stworz_plansze(self):
		matrix = [[None] * 8 for x in range(8)]

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


class Pionek:
	def __init__(self, kolor, dama = False):
		self.kolor = kolor
		self.dama = dama

class Pole:
	def __init__(self, kolor, zajecie = None):
		self.kolor = kolor
		self.zajecie = zajecie

