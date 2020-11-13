# import checkers_pygame
import numpy as np
from PIL import Image
import cv2
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
import time

style.use("ggplot")

SIZE = 8
HM_EPISODES = 2
MOVE_PENALTY = 1
LOSING_CHECKER_PENALTY = 100
CAPTURING_CHECKER_REWARD = 100
epsilon = 0.5
EPS_DECAY = 0.3
SHOW_EVERY = 1

start_q_table = None

LEARNING_RATE = 0.1
DISCOUNT = 0.95

PLAYER_N = 1
PLAYER_KING_N = 2
ENEMY_N = 3
ENEMY_KING_N = 4

turn = False

d = {1: (255, 0, 0),
	 2: (255, 125, 0),
	 3: (0, 0, 255),
	 4: (0, 125, 255)}

class Checker:
	def __init__(self):
		self.x = np.random.randint(0, SIZE)
		self.y = np.random.randint(0, SIZE)
		self.capturing = False
	
	def __str__(self):
		return f"{self.x}, {self.y}"

	def __sub__(self, other):
		return (self.x - other.x, self.y - other.y)

	def action(self, choice):
		if choice == 0 and self.capturing == False:
			self.move(x = 1, y = 1)
		if choice == 1 and self.capturing == False:
			self.move(x = -1, y = -1)
		if choice == 2 and self.capturing == False:
			self.move(x = -1, y = 1)
		if choice == 3 and self.capturing == False:
			self.move(x = 1, y = -1)
		if choice == 4 and self.capturing == True:
			self.move(x = 2, y = -2)
		if choice == 5 and self.capturing == True:
			self.move(x = 2, y = 2)
		if choice == 6 and self.capturing == True:
			self.move(x = -2, y = -2)
		if choice == 7 and self.capturing == True:
			self.move(x = -2, y = 2)

	def move(self, x = False, y = False):
		if not x and not self.capturing:
			self.x += np.random.randint(-1, 2)
		elif not x:
			self.x += np.random.randint(-2, 3)
		else:
			self.x += x

		if not y and not self.capturing:
			self.y += np.random.randint(-1, 2)
		elif not y:
			self.y += np.random.randint(-2, 3)
		else:
			self.y += y
			
		if self.x < 0:
			self.x = 0
		elif self.x > SIZE - 1:
			self.x = SIZE - 1
		
		if self.y < 0:
			self.y = 0
		elif self.y > SIZE - 1:
			self.y = SIZE - 1

if start_q_table is None:
	q_table = {}
	for x1 in range(-SIZE+1, SIZE):
		for y1 in range(-SIZE+1, SIZE):
			for x2 in range(-SIZE+1, SIZE):
				for y2 in range(-SIZE+1, SIZE):
					q_table[(x1, y1),(x2, y2)] = [np.random.uniform(-5, 0) for i in range(8)]
else:
	with open(start_q_table, "rb") as f:
		q_table = pickle.load(f)

episode_rewards = []
for episode in range(HM_EPISODES):


	player = Checker()
	enemy = Checker()
	if episode % SHOW_EVERY == 0:
		print(f"on # {episode}, epsilon: {epsilon}")
		print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
		show = True
	else:
		show = False

	episode_reward = 0
	for i in range(200):
		if turn == True:
			turn = False
		else:
			turn = True
		obs = (player - enemy, player-enemy)
		if np.random.random() > epsilon:
			action = np.argmax(q_table[obs])
		else:
			action = np.random.randint(0,8)

		if turn == True:
			player.action(action)
		else:
			enemy.move()

		if (player.x + 1 == enemy.x or player.x - 1 == enemy.x) and (player.y + 1 == enemy.y or player.y - 1 == enemy.y) and not turn:
			reward = - LOSING_CHECKER_PENALTY
		elif (player.x + 1 == enemy.x or player.x - 1 == enemy.x) and (player.y + 1 == enemy.y or player.y - 1 == enemy.y) and turn:
			reward = CAPTURING_CHECKER_REWARD
		else:
			reward = -MOVE_PENALTY

		new_obs = (player - enemy, player-enemy)
		max_future_q = np.max(q_table[new_obs])
		current_q = q_table[obs][action]

		if reward == CAPTURING_CHECKER_REWARD:
			new_q = CAPTURING_CHECKER_REWARD
		elif reward == -LOSING_CHECKER_PENALTY:
			new_q = -LOSING_CHECKER_PENALTY
		else:
			new_q = (1-LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

		q_table[obs][action] = new_q

		if show:
			env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
			env[player.y][player.x] = d[PLAYER_N]
			env[enemy.y][enemy.x] = d[ENEMY_N]

			img = Image.fromarray(env, "RGB")
			img = img.resize((300,300))
			cv2.imshow("", np.array(img))
			if reward == CAPTURING_CHECKER_REWARD or reward == -LOSING_CHECKER_PENALTY:
				if cv2.waitKey(500) & 0xFF == ord("q"):
					break
			else:
				if cv2.waitKey(1) & 0xFF == ord("q"):
					break

		episode_reward += reward
		if reward == CAPTURING_CHECKER_REWARD or reward == -LOSING_CHECKER_PENALTY:
			break
		
	episode_rewards.append(episode_reward)
	epsilon *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable- {int(time.time())}.pickle", "wb") as f:
	pickle.dump(q_table, f)

# RED 	   = (255,   0,   0)
# RED_QUEEN  = (255, 255,   0)
# BLUE 	   = (  0,   0, 255)
# BLUE_QUEEN = (  0, 255, 255)

# class Bot:
# 	def __init__(self):
# 		self.color = BLUE
# 		self.queen = BLUE_QUEEN
# 		self.all_possible_moves = []
# 		self.possible_checkers = []
# 		pass
	
# 	def move(self, board):
# 		self.possible_checkers = []
# 		move = self.best_move(board)
# 		# checker
# 		return move

# 	def best_move(self, board):
# 		self.calculate_value(board)
# 		self.set_possible_checkers(board)
# 		self.set_all_possible_moves(board)

# 	def set_possible_checkers(self, board):
# 		for i in range(8):
# 			for j in range(8):
# 				if hasattr(self.board_occ(board,i,j), "kolor") == True:
# 					if self.board_occ(board,i,j).kolor == self.color or self.board_occ(board,i,j).kolor == self.queen:
# 						self.possible_checkers.append([i,j])
# 		print(self.possible_checkers)

# 	def set_all_possible_moves(self, board):
# 		"ruchy muszą być w takiej formie [	wszystkie ruchy[	wszystkie ruchy pionka[	ruch 1	][	ruch 0	]	]	]"
# 		for i in range(8):
# 			for j in range(8):
# 				if hasattr(self.board_occ(board, i, j), "kolor") == True:
# 					if self.board_occ(board,i,j).kolor == self.color or self.board_occ(board,i,j).kolor == self.queen:
# 						pass
	
# 	def checkers_posibble_moves(self, board, x, y):
# 		pass

# 	def adjecent_possible_moves(self, board, x, y):
# 		pass

# 	def calculate_value(self, board):
# 		num_red_pieces = 0
# 		num_red_queens = 0
# 		num_blue_pieces = 0
# 		num_blue_queens = 0
# 		for i in range(8):
# 			for j in range(8):
# 				if hasattr(self.board_occ(board,i,j), "kolor") == True:
# 					if self.board_occ(board,i,j).kolor == RED:
# 						num_red_pieces += 1
# 					elif self.board_occ(board,i,j).kolor == RED_QUEEN:
# 						num_red_queens += 1
# 					elif self.board_occ(board,i,j).kolor == BLUE:
# 						num_blue_pieces += 1
# 					elif self.board_occ(board,i,j).kolor == BLUE_QUEEN:
# 						num_blue_queens += 1
# 		"równanie obliczające 'wartość' planszy"
# 		value = num_blue_pieces + (2 * num_blue_queens) - (num_red_pieces + (2 * num_red_queens))
# 		print(value)
# 		return value
	
# 	def board_occ(self, board, x, y):
# 		return board[x][y].zajecie


