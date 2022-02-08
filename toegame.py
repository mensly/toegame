#!/usr/bin/python3
from random import shuffle

DEFAULT_SYMBOLS = list('XOLGBTIQ')
LINE = {-1: ' ', 0: ' ', 1: ' '}

class InvalidDimensionException():
 pass

class ToeGame():
 def __init__(self):
  self.players = 0
  self.symbols = []
  self.dimensions = 0
  self.grid = []
  self.playing = True

 def setup_grid(self, dimensions):
  self.dimensions = dimensions
  if dimensions < 4:
   self.setup_players(dimensions)
   if dimensions == 0:
    self.grid = [' ']
   elif dimensions == 1:
    self.grid = LINE.copy()

 def setup_players(self, players, symbols=DEFAULT_SYMBOLS):
  self.players = players
  shuffle(symbols)
  self.symbols = symbols[0:players]
 
 def input_turn(self):
  self.print_grid() # TODO: Interactive version to input
  pass

 def check_win(self):
  if self.dimensions == 0:
   return self.grid[0]
  elif self.dimensions == 1 and len(set(self.grid)) == 1:
   return self.grid[0]
  # TODO: Check for line through any dimensional pathway 
  return None
  
 def print_grid(self):
  if self.dimensions == 0:
   self.print_grid_0()
  if self.dimensions == 1:
   self.print_grid_1()

 def print_grid_0(self):
  print('_' * 3)
  print(f'|{self.grid[0]}|')
  print('-' * 3)

 def print_grid_1(self):
  print('_' * (1 + 2 * 3))
  print('|')
  print('-' * (1 + 2 * 3))
   
if __name__ == '__main__': # TODO: Argument parsing
 game = ToeGame()
 game.setup_grid(0)
 victor = None
 while victor == None:
  game.input_turn()
  victor = game.check_win()
 game.print_grid()
 print(f'GAME OVER, Congratulations {victor}')
 
