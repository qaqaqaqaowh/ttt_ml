import random
import math
import threading

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

class AI_ALGO():
	def simulate(self, game):
		if game.over():
			return game.score()
		move = random.choice(game.valid_moves())
		game.move(move)
		score = -self.simulate(game)
		game.undo()

		return score

	def replay_score(self, game, N=100):
		scores = [self.simulate(game) for i in range(0, N)]
		return sum(scores) / len(scores)

	def ai_move(self, game):
		actions = {}
		for move in game.valid_moves():
			game.move(move)
			actions[move] = self.replay_score(game)
			game.undo()
		return max(actions, key=actions.get)

class AI_UCT():
	def __init__(self):
		self.visits = {}
		self.differential = {}

	def heusomething_value(self, game):
		N = self.visits.get("total", 1)
		Ni = self.visits.get(str(game.state()), 1e-5)
		V = self.differential.get(str(game.state()), 0) * 1.0 / Ni
		return V + 1.5 * math.sqrt(math.log(N) / Ni)

	def record(self, game, score):
		self.visits["total"] = self.visits.get("total", 1) + 1
		self.visits[str(game.state())] = self.visits.get(str(game.state()), 0) + 1
		self.differential[str(game.state())] = self.differential.get(str(game.state()), 0) + score

	def simulate(self, game, steps=math.inf):
		if steps == 0 or game.over():
			self.record(game, -game.score())
			return -game.score()

		action_heusomething = {}
		for move in game.valid_moves():
			game.move(move)
			action_heusomething[move] = self.heusomething_value(game)
			game.undo()

		move = max(action_heusomething, key=action_heusomething.get)
		game.move(move)
		score = -self.simulate(game, steps - 1)
		game.undo()
		self.record(game, score)

		return score

	def replay_score(self, game, N=250):
		for i in range(0, N):
			self.simulate(game)
		return self.differential[str(game.state())] * 1.0 / self.visits[str(game.state())]

	def ai_move(self, game):
		actions = {}
		for move in game.valid_moves():
			game.move(move)
			actions[move] = -self.replay_score(game)
			game.undo()
		return max(actions, key=actions.get)

wins = {"one": 0, "two": 0}

ai1 = AI_ALGO()
ai2 = AI_UCT()

def one_game(first, second):
	for i in range(0, 1000):
		game = TicTacToe()
		while not game.over():
			print(game)
			move = first.ai_move(game)
			# move = random.choice(game.valid_moves())
			if game.move(move) and not game.over():
				move2 = second.ai_move(game)
				game.move(move2)
		second.replay_score(game)
		if game.score() == 1:
			if len(game.moves) % 2 == 0:
				wins["two"] += 1
			else:
				wins["one"] += 1
		print(f"""
{game}\n
Player one: {wins['one']}
Player two: {wins['two']}
	""")

one_game(ai1, ai2)
one_game(ai2, ai1)

# threads = []

# for i in range(0, 100):
# 	first = ai1 if i % 2 == 0 else ai2
# 	second = ai2 if i % 2 == 0 else ai1
# 	t = threading.Thread(target=one_game,args=(first, second))
# 	threads += [t]
# 	t.start()

# print("Started all threads, joining...")

# for t in threads:
# 	t.join()

while True:
	game = TicTacToe()
	while not game.over():
		print(game)
		move = int(input("Give number: "))
		if game.move(move) and not game.over():
			move2 = ai2.ai_move(game)
			game.move(move2)
	ai2.replay_score(game)
	print(game)
	breakpoint()

# hash(frozenset({"asd": "qwe"}.items()))

