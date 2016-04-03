 # -*- coding: utf-8 -*-
import tweepy
import pickle
import random
import sys
from pprint import pprint
from env import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET

# grid dims for Twitter
WIDTH = 11
HEIGHT = 12
# nicer looping
OFFSETS = [(-1, -1), (0, -1), (1, -1),
		   (-1, 0), (1, 0),
		   (-1, 1), (0, 1), (1, 1)]


def initialize():
	"""
	states are tuples of (generation_count, grid),
	so return (0, <new random grid>)
	"""
	grid = []
	for _ in range(HEIGHT):
		row = []
		for _ in range(WIDTH):
			row.append(random.choice([True, False]))
		grid.append(row)

	# new forest, but the forest spirit is dead....
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = tweepy.API(auth)
	api.update_status("You would do that? Kill the very heart of the forest?")
	api.update_status("Even if all the trees grow back, it won't be his forest anymore. The Forest Spirit is dead.")
	return (0, grid)


def step(state):
	"""
	return the next generation
	"""
	n = state[0]
	grid = state[1]
	new_grid = []

	for j, row in enumerate(grid):
		new_row = []
		for i, cell in enumerate(row):
			living_neighbors = 0
			for di, dj in OFFSETS:
				# wraparound boundary conditions
				x = i + di if i + di < WIDTH else 0
				y = j + dj if j + dj < HEIGHT else 0
				if grid[y][x]:
					living_neighbors += 1
			new_row.append(cell and living_neighbors == 2 or living_neighbors == 3)
		new_grid.append(new_row)

	return (n + 1, new_grid)


def string_of_cell(cell):
	return "🌳" if cell else "🌱"


def string_of_grid(grid):
	"""
	emojify the grid
	"""
	ret = ""
	for row in grid:
		ret += "".join(string_of_cell(cell) for cell in row) + " "
	return ret


if __name__ == "__main__":
	sys.stdout.write("LifeBot")
	# initialize, or load state if there is one ***************************** #
	try:
		with open("state.pickle", 'rb') as f:
			sys.stdout.write("Load state from file ...")
			state = pickle.load(f)
	except FileNotFoundError:
		sys.stdout.write("Initialize new state ...")
		state = initialize()

	sys.stdout.write("... state is:")
	pprint(state)
	# regenerate if it's getting stale
	if state[0] > 100:
		sys.stdout.write("Old forest. Burn it down!")
		state = initialize()

	# generate next state *************************************************** #
	state = step(state)

	# authenticate ********************************************************** #
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = tweepy.API(auth)

	# tweet state *********************************************************** #
	tweet = string_of_grid(state[1])
	sys.stdout.write("Tweeting...")
	# sys.stdout.write(tweet)
	stat = api.update_status(tweet)
	sys.stdout.write("Tweeted with status:")
	pprint(stat)

	# save state to disk **************************************************** #
	with open("state.pickle", "wb") as f:
		sys.stdout.write("Saving the new state, ...")
		pprint(state)
		pickle.dump(state, f)
		sys.stdout.write("Success. Til next time!")

