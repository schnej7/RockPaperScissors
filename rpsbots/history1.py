from __future__ import division
import random
import itertools


OPTIONS = ["R", "P", "S"]
BEAT = {
  "R": "P",
  "P": "S",
  "S": "R",
}

ALPHA = (1/3) + 0.01

def product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


class MarkovPredictor:
   '''
   Using the markov assumption with k=length, count n-sequences.
   Allow requests for predictions of the most likely next state
   '''
   
   def __init__(self, options, length):
      self.options = options
      self.length = length
      self.history = []
      self.counts = {}
      self.total = 0

      # LaPlace Smooth
      all_seqs = product(options, repeat=length)
      for ngram in all_seqs:
         self.counts[ngram] = 1
         self.total += 1
       

   def observe(self, item):
      self.history.append(item)
      if len(self.history) > self.length:
         self.history.pop(0)

      if len(self.history) == self.length:
         ngram = tuple(self.history)
         if ngram in self.counts:
            self.counts[ngram] +=  1
            self.total += 1
         else:
            print "%s not in %s" % (str(ngram), str(self.counts))

   def predict(self):
    
      if len(self.history) < self.length:
         return None, 0
       
      counts = {}
      total = 0
      for option in self.options:
         ngram = tuple(self.history[-1 * (self.length - 1):]) + (option,)
         counts[option] = self.counts[ngram]
         total += counts[option]

      best_option = None
      best_chance = 0
      for option in self.options:
         chance = counts[option] / total
         if chance > best_chance:
            best_chance = chance
            best_option = option

      return best_option, best_chance

# Base strategy: make a random move
output = random.choice(OPTIONS)


if input == '':
    # Hypothesis: people think about 4 moves back when playing
    predictors = [MarkovPredictor(OPTIONS, length) for length in range(2,4)]

else:
    for p in predictors:
       p.observe(input)

    choices = [p.predict() for p in predictors]
    best_choice = None
    best_chance = 0
    
    for choice, chance in choices:
       if chance > best_chance:
          best_chance = chance
          best_choice = choice

    if best_chance - ALPHA > 0:
        output = BEAT[best_choice]
