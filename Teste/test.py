from ple.games.catcher import Catcher
from ple import PLE
import numpy as np
import random
class MyAgent:
	def __init__(self, actions):
		self.actions = actions
		self.politc = {}
		self.randomFactory = 500

	def maxPick(self, state):
		j = None
		for i in self.politc[state].keys():
			if self.politc[state][i] > self.politc[state][j]:
				j = i
		return j

	def pickAction(self, state):
		if state not in self.politc.keys():
			self.politc[state] = {97: 0, 100: 0, None: 0}
		if random.randint(0, 100) < self.randomFactory:
			self.randomFactory -= random.randint(0, 2)
			return self.actions[np.random.randint(0, len(self.actions))]
		return self.maxPick(state)

	def pickValue(self, state, action):
		print(self.politc[state][action])
		return self.politc[state][action]

	def updatePolitc(self, reward, state, action):
		self.politc[state][action] = reward

def myreward(state, action):
	print(state, action)
	if state['player_x'] > state['fruit_x'] and action == 97:
		return 1
	if state['player_x'] > state['fruit_x'] and action == 100:
		return -1
	if state['player_x'] > state['fruit_x'] and action == None:
		return -1
	if state['player_x'] < state['fruit_x'] and action == 97:
		return -1
	if state['player_x'] < state['fruit_x'] and action == 100:
		return 1
	if state['player_x'] < state['fruit_x'] and action == None:
		return -1
	if state['player_x'] == state['fruit_x'] and action == None:
		return 2
	if state['player_x'] == state['fruit_x'] and action == 97:
		return -2
	if state['player_x'] == state['fruit_x'] and action == 100:
		return -2

game = Catcher(width=256, height=256, init_lives=3)

p = PLE(game, fps=30, display_screen=True, force_fps=False)
p.init()
myAgent = MyAgent(p.getActionSet())
print(p.getActionSet())
nb_frames = 100000
reward = 0.0
randomFactory = 200

for f in range(nb_frames):
	if p.game_over(): #check if the game is over
		p.reset_game()

	state = game.getGameState()
	obs = str(state['player_x'])+ " " + str(state['fruit_x'])
	action = myAgent.pickAction(obs)
	reward = myreward(state, action)
	
	p.act(action)

	state1 = game.getGameState()
	obs1 = str(state['player_x'])+ " " + str(state['fruit_x'])
	action1 = myAgent.pickAction(obs)
	reward1 = myreward(state, action)

	myAgent.updatePolitc(myAgent.pickValue(obs, action) + 0.1*(reward + 0.9*(myAgent.pickValue(obs1, action1) - myAgent.pickValue(obs, action)) ), obs, action)