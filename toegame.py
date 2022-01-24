#!/usr/bin/python3

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
  if dimensions == 0:
   self.playing = False

 def setup_players(self):
  if self.dimensions < 3:
   self.players = self.dimensions 

 def print_grid(self):
  if self.dimensions < 0 or self.dimensions > 2: # TODO: Add 3D and 4D
   pass

 def input_turn(self):
  print('TODO: Input turn')



if __name__ == '__main__':
 # TODO: Argument parsing
 print('Toe Game with Any Dimension')
 game = ToeGame()
 game.setup_grid(0)
 game.setup_players()
 while game.playing:
  game.print_grid()
  game.input_turn()
 print('GAME OVER')
 
