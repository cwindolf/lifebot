import pickle

with open("state.pickle", "wb") as f:
	state = pickle.load(f)
	pickle.dump((101, state[1]), f)

