import random
import math

class TicTacToe:
	def __init__(self):
		self.moves = []

	def __str__(self):
		player_one = [move for i, move in enumerate(self.moves) if i % 2 == 0]
		player_two = [move for i, move in enumerate(self.moves) if i % 2 == 1]

		row_string = "-------\n"
		for y in range(0,3):
			row_string += "|"
			for x in range(0,3):
				pos = y * 3 + x
				if pos in player_one:
					row_string += "O"
				elif pos in player_two:
					row_string += "X"
				else:
					row_string += " "
				row_string += "|"
			row_string += "\n-------\n"
		return row_string

	def state(self):
		player_one = [move for i, move in enumerate(self.moves) if i % 2 == 0]
		player_two = [move for i, move in enumerate(self.moves) if i % 2 == 1]
		return ["O" if i in player_one else ("X" if i in player_two else None) for i in range(0,9)]

	def undo(self):
		self.moves.pop()

	def move(self, move):
		if move in self.moves:
			return False
		else:
			self.moves += [move]
			return True

	def over(self):
		return self.check_win() or len(self.moves) == 9

	def score(self):
		return self.check_win()

	def valid_moves(self):
		return list(set({0,1,2,3,4,5,6,7,8}).difference(set(self.moves)))

	def check_win(self):
		win_conds = [
			[0,1,2],
			[3,4,5],
			[6,7,8],
			[0,3,6],
			[1,4,7],
			[2,5,8],
			[0,4,8],
			[2,4,6]
		]
		player_one = [move for i, move in enumerate(self.moves) if i % 2 == 0]
		player_two = [move for i, move in enumerate(self.moves) if i % 2 == 1]

		for win_cond in win_conds:
			if len(set(player_one).intersection(set(win_cond))) == 3 or len(set(player_two).intersection(set(win_cond))) == 3:
				return 1
		return 0

def heusomething_value(game):
	N = visits.get("total", 1)
	Ni = visits.get(hash(tuple(game.state())), 1e-5)
	V = differential.get(hash(tuple(game.state())), 0) * 1.0 / Ni
	return V + 0.3 * math.sqrt(math.log(N) / Ni)

def record(game, score):
	visits["total"] = visits.get("total", 1) + 1
	visits[hash(tuple(game.state()))] = visits.get(hash(tuple(game.state())), 0) + 1
	differential[hash(tuple(game.state()))] = differential.get(hash(tuple(game.state())), 0) + score

def simulate(game):
	if game.over():
		record(game, -game.score())
		return -game.score()

	action_heusomething = {}
	for move in game.valid_moves():
		game.move(move)
		action_heusomething[move] = -heusomething_value(game)
		game.undo()

	move = max(action_heusomething, key=action_heusomething.get)
	game.move(move)
	score = -simulate(game)
	game.undo()
	record(game, score)

	return -score

def replay_score(game, N=100):
	scores = [simulate(game) for i in range(0, N)]
	return sum(scores) / len(scores)

def ai_move(game):
	actions = {}
	for move in game.valid_moves():
		game.move(move)
		actions[move] = replay_score(game)
		game.undo()
	return max(actions, key=actions.get)

visits = {}
differential = {}

for _ in range(0, 100):
	game = TicTacToe()
	while not game.over():
		print(game)
		move = random.choice(game.valid_moves())
		if game.move(move) and not game.over():
			move2 = ai_move(game)
			game.move(move2)
	print(game)

while True:
	game = TicTacToe()
	while not game.over():
		print(game)
		move = int(input("Give number: "))
		if game.move(move) and not game.over():
			move2 = ai_move(game)
			game.move(move2)
	print(game)
	breakpoint()

# hash(frozenset({"asd": "qwe"}.items()))

