#!/usr/bin/python3
import curses
from random import shuffle

DEFAULT_SYMBOLS = 'XOLGBTIQ'
BLANK = ' '
LINE = {-1: BLANK, 0: BLANK, 1: BLANK}

class InvalidDimensionException():
 pass

class ToeGame():
 def __init__(self):
  self.players = 0
  self.player = 0
  self.symbols = []
  self.dimensions = 0
  self.grid = []
  self.playing = True
  self.x_offset = 0
  self.y_offset = 0
  self.pos = []

 @property
 def center(self):
  return [self.y_offset, self.x_offset]

 @property
 def cursor(self):
  cursor = self.center
  if self.dimensions == 0: return cursor
  cursor[0] = cursor[0] + 2 * self.pos[0]
  if self.dimensions == 0: return cursor
  # TODO: Add higher dimensions
  return cursor

 @property
 def player_symbol(self):
  return self.symbols[self.player]

 @player_symbol.setter
 def player_symbol(self, value):
  self.symbols[self.player] = chr(value)

 def setup_grid(self, dimensions, y_offset, x_offset):
  self.dimensions = dimensions
  self.y_offset = y_offset
  self.x_offset = x_offset
  self.pos = [0] * max(2, dimensions)
  if dimensions < 4:
   self.setup_players(dimensions)
   if dimensions == 0:
    self.grid = [BLANK]
   elif dimensions == 1:
    self.grid = LINE.copy()

 def setup_players(self, players):
  self.players = players
  self.symbols = list(BLANK * players)

 def apply_movement(self, key):
  # TODO: Support movement at edges to support higher dimensions
  if key == curses.KEY_UP:
   self.pos[0] = max(self.pos[0] - 1, -1)
   return None
  elif key == curses.KEY_DOWN:
   self.pos[0] = min(self.pos[0] + 1, 1)
   return None
  return key
 
 def input_turn(self, stdscr):
  stdscr.refresh()
  self.print_grid(stdscr)
  stdscr.move(1 + self.y_offset + (self.pos[1] + 1) * 2, 
   1 + self.x_offset + (self.pos[0] + 1) * 2)
  if self.dimensions == 0:
   stdscr.getch()
   return
  key = None
  while not key or self.player_symbol == BLANK:
   key = stdscr.getch()
   if self.player_symbol == BLANK and chr(key).isprintable():
    self.player_symbol = key
   key = self.apply_movement(key)
   stdscr.move(1 + self.y_offset + self.pos[1] * 2, 
    1 + self.x_offset + self.pos[0] * 2)
  self.grid[self.pos[0]] = self.player_symbol
  self.player = (self.player + 1) % self.players

 def check_win(self):
  if self.dimensions == 0:
   return self.grid[0]
  elif self.dimensions == 1 and len(set(self.grid.values())) == 1:
   return self.grid[0]
  # TODO: Check for line through any dimensional pathway 
  return None
  
 def print_grid(self, stdscr):
  if self.dimensions == 0:
   self.print_grid_0(stdscr)
  if self.dimensions == 1:
   self.print_grid_1(stdscr)

 def print_grid_0(self, stdscr):
  stdscr.addstr(2 + self.y_offset, 2 + self.x_offset, '_' * 3)
  stdscr.addstr(3 + self.y_offset, 2 + self.x_offset, f'|{self.grid[0]}|')
  stdscr.addstr(4 + self.y_offset, 2 + self.x_offset, '-' * 3)

 def print_grid_1(self, stdscr):
  stdscr.addstr(self.y_offset, self.x_offset, '_' * (1 + 2 * 3))
  for i in range(-1, 2):
   stdscr.addstr(i * 2 + self.y_offset, self.x_offset, f'|{self.grid[i]}|')
   stdscr.addstr(i * 2 + self.y_offset + 1, self.x_offset, '-' * (1 + 2 * 3))
  
def main(stdscr):
 game = ToeGame()
 game.setup_grid(0, 8, 8)
 victor = None
 while victor == None:
  stdscr.clear()
  stdscr.addstr(0, 0, str(game.grid))
  game.input_turn(stdscr)
  victor = game.check_win()
 game.print_grid(stdscr)
 return victor

if __name__ == '__main__':
 victor = curses.wrapper(main)
 print(f'Game Over, Congratulations {victor}')
 


 
