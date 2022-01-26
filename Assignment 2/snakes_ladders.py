import sys
sys.path.append("../")
from dataclasses import dataclass
from typing import Mapping, Dict, Sequence, Iterable
from rl.distribution import Categorical, FiniteDistribution, Constant, Distribution
from rl.markov_process import FiniteMarkovProcess, NonTerminal, Terminal 
import matplotlib.pyplot as plt
import itertools


@dataclass(frozen=True)
class State:
	position : int 



class SnakesAndLaddersMP(FiniteMarkovProcess[State]):
	def __init__(self, from_to : Mapping[State, State]):
		self.from_to = from_to
		super().__init__(self.get_transition_map())
		print("Generated the Markov Process")


	def get_transition_map(self) -> Mapping[State, FiniteDistribution[State]]:
		d : Dict[State, FiniteDistribution[State]] = {}

		for state in range(1, 100):
			state_probs_map = {}
			next_state = 0
			
			for j in range(state + 1, min(101, state + 7)):
				if j in self.from_to.keys():
					next_state = self.from_to[j]
				else:
					next_state = j

				state_probs_map[State(position = next_state)] = 1. / 6.

			if state > 94:
				state_probs_map[State(position = state)] = (state - 94.) / 6.

			d[State(position = state)] = Categorical(state_probs_map)

		return d



if __name__ == '__main__':
	changes_from = [1, 4, 9, 28, 36, 21, 51, 71, 80, \
				    16, 47, 49, 56, 64, 87, 93, 95, 98]
	changes_to = [38, 14, 31, 84, 44, 42, 67, 91, 100, \
				   6, 26, 11, 53, 60, 24, 73, 75, 78]

	from_to = {fr : to for fr, to in zip(changes_from, changes_to)}
	game = SnakesAndLaddersMP(from_to = from_to)

	
	# print("Transition Map")
	# print("----------------")
	# print(game)


	start_distribution = Constant(value = NonTerminal(State(position = 1)))
	num_traces = 10

	outcomes = [len([st for st in it]) for it in itertools.islice(game.traces(start_distribution), num_traces)]
	print(outcomes)
	
	
	plt.hist(outcomes)
	plt.xlabel('Time to complete a game of SNakes and Ladders')
	plt.ylabel('Frequency')
	plt.title("Probability Distribution of the Time Taken to Finish Snakes and Ladders")

	plt.show()

