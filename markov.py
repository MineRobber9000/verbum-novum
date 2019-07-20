import random

class MarkovWord:
	"""2nd order markov chain for making words"""
	def __init__(self):
		self.brain = dict(START=[])
	def train(self,word):
		letters = list(word)
		n = len(letters)
		self.brain["START"].append((letters[0],letters[1]))
		for i,l1 in enumerate(letters):
			if n>(i+2):
				l2 = letters[i+1]
				lt = letters[i+2]
				if (l1,l2) in self.brain:
					self.brain[(l1,l2)].append(lt)
				else:
					self.brain[(l1,l2)]=[lt]
		end=(letters[-2],letters[-1])
		if end in self.brain:
			self.brain[end].append("END")
		else:
			self.brain[end]=["END"]
	def newWord(self):
		base = random.choice(self.brain["START"])
		out = "".join(base)
		last, next = base
		r = random.choice(self.brain[(last,next)])
		while r!="END":
			out+=r
			last = next
			next = r
			r = random.choice(self.brain[(last,next)])
		return out
