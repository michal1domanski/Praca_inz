import random
import numpy as np
import copy
import math

RED 	   = (255,   0,   0)
RED_QUEEN  = (255, 255,   0)
BLUE 	   = (  0,   0, 255)
BLUE_QUEEN = (  0, 255, 255)

class Bot:
	def __init__(self, max_depth):
		self.color = RED
		self.queen = RED_QUEEN
		self.all_possible_moves = []
		self.possible_checkers = []
		self.max_depth = max_depth
		self.lowest_board_number = (0, 0)
		self.highest_board_number = (0, 0)
		self.capturing = False

	def move(self, board, moves):
		# wybieram ruch do wykonania i przekazuje go do main.py
		self.color = RED
		self.queen = RED_QUEEN
		if moves == None:
			exit
		else:
			self.all_possible_moves, self.possible_checkers = moves
		board = self.max_fun_AB(board, -400, 400, 0)
		# board = self.max_fun(board, 0)
		move = self.highest_board_number
		return move

	def min_fun(self, board, depth):
		if depth >= self.max_depth:
			board_score = self.calculate_value(board)
			return board_score

		if self.color == BLUE:
			self.color = RED
			self.queen = RED_QUEEN
		else:
			self.color = BLUE
			self.queen = BLUE_QUEEN

		next_moveset = self.generate_new_board(board)
		self.lowest_board_number = (0, 0)
		lowest_score = 1000
		for i in range(len(next_moveset)):
			for j in range(len(next_moveset[i])):
				self.all_possible_moves, self.possible_checkers = self.moveset_for_new_board(next_moveset[i][j], self.color)
				score = self.max_fun(next_moveset[i][j], depth + 1)
				if score < lowest_score:
					self.lowest_board_number = (i, j)
					lowest_score = score

		return lowest_score

	def max_fun(self, board, depth):
		if depth >= self.max_depth:
			board_score = self.calculate_value(board)
			return board_score

		if self.color == BLUE:
			self.color = RED
			self.queen = RED_QUEEN
		else:
			self.color = BLUE
			self.queen = BLUE_QUEEN

		next_moveset = self.generate_new_board(board)
		self.highest_board_number = (0, 0)
		highest_score = -1000
		for i in range(len(next_moveset)):
			for j in range(len(next_moveset[i])):
				self.all_possible_moves, self.possible_checkers = self.moveset_for_new_board(next_moveset[i][j], self.color)
				if self.color == BLUE and self.capturing == True:
					score = -200
				else:
					score = self.min_fun(next_moveset[i][j], depth + 1)
				if score > highest_score:
					self.highest_board_number = (i, j)
					highest_score = score
		return highest_score

	def min_fun_AB(self, board, alpha, beta, depth):
		if depth >= self.max_depth:
			board_score = self.calculate_value(board)
			return(board_score)
		
		next_moveset = self.generate_new_board(board)
		self.lowest_board_number = (0, 0)
		lowest_score = 300
		for i in range(len(next_moveset)):
			for j in range(len(next_moveset[i])):
				self.all_possible_moves, self.possible_checkers = self.moveset_for_new_board(next_moveset[i][j], self.color)
				if self.color == BLUE and self.capturing == True:
					score = self.min_fun_AB(next_moveset[i][j], alpha, beta, depth + 1)
				else:
					self.capturing = False
					self.color = RED
					self.queen = RED_QUEEN
					score = self.max_fun_AB(next_moveset[i][j], alpha, beta, depth + 1)
	
				if score < lowest_score:
					self.lowest_board_number = (i, j)
					lowest_score = score
				elif depth == 0 and score == lowest_score:
					if random.random() < 0.3:
						self.lowest_board_number = (i, j)
				
				if score < alpha:
					return lowest_score
				if score < beta:
					beta = score

		if depth == 0:
			return next_moveset[self.lowest_board_number[0]][self.lowest_board_number[1]]
		
		return lowest_score

	def max_fun_AB(self, board, alpha, beta, depth):
		if depth >= self.max_depth:
			board_score = self.calculate_value(board)
			return(board_score)
		
		next_moveset = self.generate_new_board(board)
		self.highest_board_number = (0, 0)
		highest_score = -300
		for i in range(len(next_moveset)):
			for j in range(len(next_moveset[i])):
				self.all_possible_moves, self.possible_checkers = self.moveset_for_new_board(next_moveset[i][j], self.color)
				if self.color == RED and self.capturing == True:
					score = self.max_fun_AB(next_moveset[i][j], alpha, beta, depth + 1)
				else:
					self.capturing = False
					self.color = BLUE
					self.queen = BLUE_QUEEN
					score = self.min_fun_AB(next_moveset[i][j], alpha, beta, depth + 1)

				if score > highest_score:
					self.highest_board_number = (i, j)
					highest_score = score
				elif depth == 0 and score == highest_score:
					if random.random() < 0.3:
						self.highest_board_number = (i, j)
				
				if score > beta:
					return highest_score
				if score > alpha:
					alpha = score

		if depth == 0:
			return next_moveset[self.highest_board_number[0]][self.highest_board_number[1]]
			
		
		return highest_score

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

	def available_moves_for_piece(self, board, x, y):
		possible_moves = []
		if board[x][y].zajecie != None:
			if self.end_side_tile(y) == 1:
				if self.end_top_tile(x) == 1:
					if board[x+1][y+1].zajecie == None:
						possible_moves.append([x+1, y+1]) #lewa góra planszy
				elif self.end_top_tile(x) == 2:
					if board[x-1][y+1].zajecie == None:
						possible_moves.append([x-1, y+1]) #lewy dół planszy
				elif self.end_top_tile(x) == 0: #lewa strona wszystkie moliwości
					if board[x-1][y+1].zajecie == None and board[x+1][y+1].zajecie == None:
						possible_moves.append([x-1, y+1])
						possible_moves.append([x+1,y+1])
					elif board[x-1][y+1].zajecie == None:
						possible_moves.append([x-1,y+1])
					elif board[x+1][y+1].zajecie == None:
						possible_moves.append([x+1,y+1])
			elif self.end_side_tile(y) == 2:
				if self.end_top_tile(x) == 1:
					if board[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y-1]) #prawa góra planszy
				elif self.end_top_tile(x) == 2:
					if board[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1]) #prawy dół planszy
				elif self.end_top_tile(x) == 0: #prawa strona wszystkie moliwości
					if board[x-1][y-1].zajecie == None and board[x+1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1])
						possible_moves.append([x+1,y-1])
					elif board[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1])
					elif board[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y-1])
			elif self.end_side_tile(y) == 0:
				if self.end_top_tile(x) == 1:
					if board[x+1][y+1].zajecie == None and board[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y+1])
						possible_moves.append([x+1,y-1])
					elif board[x+1][y+1].zajecie == None:
						possible_moves.append([x+1,y+1])
					elif board[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y-1])
				elif self.end_top_tile(x) == 2:
					if board[x-1][y+1].zajecie == None and board[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y+1])
						possible_moves.append([x-1,y-1])
					elif board[x-1][y+1].zajecie == None:
						possible_moves.append([x-1,y+1])
					elif board[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1])
				elif self.end_top_tile(x) == 0:
					if board[x+1][y+1].zajecie == None:
						possible_moves.append([x+1,y+1])
					if board[x+1][y-1].zajecie == None:
						possible_moves.append([x+1,y-1])
					if board[x-1][y+1].zajecie == None:
						possible_moves.append([x-1,y+1])
					if board[x-1][y-1].zajecie == None:
						possible_moves.append([x-1,y-1])
		return possible_moves
		
	def moveset_for_new_board(self, board, board_color):
		if board_color == BLUE:
			board_queen_color = BLUE_QUEEN
		else:
			board_queen_color = RED_QUEEN

		all_moves = []
		all_checkers = []
		for i in range(8):
			for j in range(8):
				if hasattr(board[i][j].zajecie, "kolor"):
					if board[i][j].zajecie.kolor == board_color or board[i][j].zajecie.kolor == board_queen_color:
						if self.possible_capturing(board,i,j) != []:
							all_moves.append(self.possible_capturing(board,i,j))
							all_checkers.append([i,j])
		
		if all_moves == []:
			self.capturing = False
			for i in range(8):
				for j in range(8):
					if hasattr(board[i][j].zajecie, "kolor"):
						if board[i][j].zajecie.kolor == board_color or board[i][j].zajecie.kolor == board_queen_color:
							if self.available_moves_for_piece(board, i, j) != []:
								all_moves.append(self.available_moves_for_piece(board, i, j))
								all_checkers.append([i, j])
		else:
			self.capturing = True

		return all_moves, all_checkers

	def possible_capturing(self, board, x, y):
		self.mozliwe_bicie = []

		self.gracz = board[x][y].zajecie.kolor

		if self.gracz == BLUE:
			self.damka = BLUE_QUEEN
		elif self.gracz == RED:
			self.damka = RED_QUEEN
		elif self.gracz == BLUE_QUEEN:
			self.gracz = BLUE
			self.damka = BLUE_QUEEN
		elif self.gracz == RED_QUEEN:
			self.gracz = RED
			self.damka = RED_QUEEN

		if board[x][y].zajecie.dama == False:
			for i in range(len(self.pola_obok(x,y))):
				if hasattr(board[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie, "kolor") == True:
					if board[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie.kolor != self.gracz and board[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie.kolor != self.damka:
						self.wrog = [self.pola_obok(x,y)[i][0],self.pola_obok(x,y)[i][1]]
						self.linia = [(x - self.wrog[0])*2, (y - self.wrog[1])*2]
						self.ruch_bicia = [x - self.linia[0], y - self.linia[1]]
						if (self.ruch_bicia[0] <= 7 and self.ruch_bicia[0] >= 0) and (self.ruch_bicia[1] <= 7 and self.ruch_bicia[1] >= 0):
							if board[self.ruch_bicia[0]][self.ruch_bicia[1]].zajecie == None:
								self.mozliwe_bicie.append([x-self.linia[0], y-self.linia[1]])
		else:
			pola_dostepne = self.queen_move(board, x, y) #dodaj te metodę
			for i in range(len(pola_dostepne)):
				odleglosc = [pola_dostepne[i][0] - x, pola_dostepne[i][1] - y]
				kierunek_ruchu = [math.floor(odleglosc[0]/abs(odleglosc[0])), math.floor(odleglosc[1]/abs(odleglosc[1]))]
				pole_wrogiego_pionka = [pola_dostepne[i][0] + kierunek_ruchu[0], pola_dostepne[i][1] + kierunek_ruchu[1]]
				pole_po_biciu = [pole_wrogiego_pionka[0] + kierunek_ruchu[0], pole_wrogiego_pionka[1] + kierunek_ruchu[1]]
				if pole_po_biciu[0] <=7 and pole_po_biciu[0] >= 0 and pole_po_biciu[1] <= 7 and pole_po_biciu[1] >=0:
					if pole_wrogiego_pionka[0] <=7 and pole_wrogiego_pionka[0] >= 0 and pole_wrogiego_pionka[1] <= 7 and pole_wrogiego_pionka[1] >=0:
						if board[pole_wrogiego_pionka[0]][pole_wrogiego_pionka[1]].zajecie != None and board[pole_po_biciu[0]][pole_po_biciu[1]].zajecie == None:
							if board[pole_wrogiego_pionka[0]][pole_wrogiego_pionka[1]].zajecie.kolor != self.gracz and board[pole_wrogiego_pionka[0]][pole_wrogiego_pionka[1]].zajecie.kolor != self.damka:
								self.mozliwe_bicie.append([pole_po_biciu[0], pole_po_biciu[1]])
				
			for i in range(len(self.pola_obok(x,y))):
				if hasattr(board[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie, "kolor") == True:
					if board[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie.kolor != self.gracz and board[self.pola_obok(x,y)[i][0]][self.pola_obok(x,y)[i][1]].zajecie.kolor != self.damka:
						self.wrog = [self.pola_obok(x,y)[i][0],self.pola_obok(x,y)[i][1]]
						self.linia = [(x - self.wrog[0])*2, (y - self.wrog[1])*2]
						self.ruch_bicia = [x - self.linia[0], y - self.linia[1]]
						if (self.ruch_bicia[0] <= 7 and self.ruch_bicia[0] >= 0) and (self.ruch_bicia[1] <= 7 and self.ruch_bicia[1] >= 0):
							if board[self.ruch_bicia[0]][self.ruch_bicia[1]].zajecie == None:
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

	def best_move(self, board):
		# tak ogólnie to jest narazie funkcja losująca ruch żeby było że można grać
		if len(self.possible_checkers) == 0:
			checker = random.randint(0, len(self.possible_checkers))
		else:
			checker = random.randint(0, len(self.possible_checkers)-1)
		movelol = random.randint(0, len(self.all_possible_moves[checker][0])-1)
		return checker, movelol
	
	def queen_move(self,board, x, y):
		ruchy = self.available_moves_for_piece(board, x, y)
		mozliwe_ruchy_damy = []
		kierunek = []
		for i in range(len(ruchy)):
			kierunek.append([- (x - ruchy[i][0]), - (y - ruchy[i][1])])
			while (ruchy[i][0] >= 0 and ruchy[i][0] <= 7 and ruchy[i][1] >= 0 and ruchy[i][1] <= 7): 
				if board[ruchy[i][0]][ruchy[i][1]].zajecie == None:
					mozliwe_ruchy_damy.append([ruchy[i][0], ruchy[i][1]])
					ruchy[i][0] += kierunek[i][0]
					ruchy[i][1] += kierunek[i][1]
				else:
					ruchy[i] = [9,9]
		return mozliwe_ruchy_damy

	def calculate_value(self, board):
		#oblicza wartość danej planszy
		num_red_pieces = 0
		num_red_queens = 0
		num_blue_pieces = 0
		num_blue_queens = 0
		for i in range(8):
			for j in range(8):
				if hasattr(self.board_occ(board,i,j), "kolor") == True:
					if self.board_occ(board,i,j).kolor == RED:
						num_red_pieces += 1
					elif self.board_occ(board,i,j).kolor == RED_QUEEN:
						num_red_queens += 1
					elif self.board_occ(board,i,j).kolor == BLUE:
						num_blue_pieces += 1
					elif self.board_occ(board,i,j).kolor == BLUE_QUEEN:
						num_blue_queens += 1
		# równanie obliczające wartość planszy
		value = -(num_blue_pieces + (2 * num_blue_queens)) + (num_red_pieces + (2 * num_red_queens))
		return value
	
	def board_occ(self, board, x, y):
		return board[x][y].zajecie

	def generate_new_board(self, board):
		#"tworzenie wszystkich możliwych wartości plansz po wszystkich możliwych ruchach"
		boards = [] #"zawiera wszystkie możliwe wartosći plansz"
		for i in range(len(self.possible_checkers)):
			boards.append(self.generate_new_board_for_piece(board, i))
		return boards

	def generate_new_board_for_piece(self, board, piece_n):
		# sprawdza wyniki plansz dla każdego ruchu dla danego pionka
		new_boards = []
		piece_moves = self.all_possible_moves[piece_n]
		for i in range(len(piece_moves[0])):
			copied_board = copy.deepcopy(board)
			new_boards.append(self.make_move_new_board(copied_board, piece_n, i))
			
		return new_boards

	def make_move_new_board(self, copied_board, piece_n, move_n):
		# Ta metoda ma służyć tworzeniu hipotetycznych ruchów i patrzeć na wynik planszy po wykonaniu ruchu
		bicie = False
		try:
			copied_board[self.all_possible_moves[piece_n][0][move_n][0]][self.all_possible_moves[piece_n][0][move_n][1]].zajecie = copied_board[self.possible_checkers[piece_n][0]][self.possible_checkers[piece_n][1]].zajecie
			copied_board[self.possible_checkers[piece_n][0]][self.possible_checkers[piece_n][1]].zajecie = None
		except:
			copied_board[self.all_possible_moves[piece_n][0][0]][self.all_possible_moves[piece_n][0][1]].zajecie = copied_board[self.possible_checkers[piece_n][0]][self.possible_checkers[piece_n][1]].zajecie
			copied_board[self.possible_checkers[piece_n][0]][self.possible_checkers[piece_n][1]].zajecie = None

		try:
			if abs(self.all_possible_moves[piece_n][0][0] - self.possible_checkers[piece_n][0]) == 2:
				bicie = True
		except:
			if abs(self.all_possible_moves[piece_n][0][move_n][0] - self.possible_checkers[piece_n][0]) == 2:
				bicie = True

		if bicie == False:
			return copied_board
		else:
			x = int((self.all_possible_moves[piece_n][0][0] + self.possible_checkers[piece_n][0])/2)
			y = int((self.all_possible_moves[piece_n][0][1] + self.possible_checkers[piece_n][1])/2)
			copied_board[x][y].zajecie = None
			return copied_board
