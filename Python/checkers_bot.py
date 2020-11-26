import random
import numpy as np
import copy

RED 	   = (255,   0,   0)
RED_QUEEN  = (255, 255,   0)
BLUE 	   = (  0,   0, 255)
BLUE_QUEEN = (  0, 255, 255)

class Bot:
	def __init__(self, max_depth):
		self.color = BLUE
		self.queen = BLUE_QUEEN
		self.all_possible_moves = []
		self.possible_checkers = []
		self.max_depth = max_depth

	def move(self, board, moves):
		# wybieram ruch do wykonania i przekazuje go do main.py
		self.possible_checkers = []
		test = None
		print(self.max_depth)
		if moves == None:
			exit
		else:
			self.all_possible_moves, self.possible_checkers = moves
		move = self.best_move(board)
		test = self.min_fun(test, 0)
		print("test ", test)
		# move = (possible_board_values[0], possible_board_values[0][0])
		return move

	#min fun i max fun są źle ale nie ma glowy żeby to wykminić teraz. zajmę się tym jutro, najpóźniej w piątek

	def min_fun(self, board, depth):
		if depth >= self.max_depth:
			return self.calculate_value(board)

		boards = self.generate_new_board(board)
		lowest_board_number = 0
		lowest_value = 100
		for i in range(len(boards)):
			score = self.max_fun(boards[i], depth + 1)
			if score < lowest_value:
				lowest_board_number = i
				lowest_value = score

		return lowest_value

	def max_fun(self, board, depth):
		if depth >= self.max_depth:
			return self.calculate_value(board)

		boards = self.generate_new_board(board)
		highest_board_number = 0
		highest_value = -100
		for i in range(len(boards)):
			score = self.min_fun(boards[i], depth + 1)
			if score < highest_value:
				highest_board_number = i
				highest_value = score

		if depth == 0:
			return boards[highest_board_number]

		return highest_value

	def best_move(self, board):
		# tak ogólnie to jest narazie funkcja losująca ruch żeby było że można grać
		if len(self.possible_checkers) == 0:
			checker = random.randint(0, len(self.possible_checkers))
		else:
			checker = random.randint(0, len(self.possible_checkers)-1)
		movelol = random.randint(0, len(self.all_possible_moves[checker][0])-1)
		return checker, movelol

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
		value = num_blue_pieces + (2 * num_blue_queens) - (num_red_pieces + (2 * num_red_queens))
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
