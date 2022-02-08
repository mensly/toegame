#!/usr/bin/python3
import curses
from random import shuffle

DEFAULT_SYMBOLS = 'XOLGBTIQ'
BLANK = ' '
LINE = {-1: BLANK, 0: BLANK, 1: BLANK}

class InvalidDimensionException(BaseException):
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
  return [self.x_offset, self.y_offset]

 @property
 def cursor(self):
  cursor = self.center
  if self.dimensions == 0: return cursor
  cursor[1] = cursor[1] + 2 * self.pos[0]
  if self.dimensions == 0: return cursor
  # TODO: Add higher dimensions
  return cursor

 @property
 def player_turn(self):
  if self.dimensions == 0: return BLANK
  return self.player_symbol or 'NEW'

 @property
 def player_symbol(self):
  return self.symbols[self.player]

 @player_symbol.setter
 def player_symbol(self, value):
  self.symbols[self.player] = chr(value)

 @property
 def grid_symbol(self):
  return self.grid[self.pos[0]] # TODO: Higher dimensions

 @grid_symbol.setter
 def grid_symbol(self, value):
  self.grid[self.pos[0]] = value

 def move_to_cursor(self, stdscr):
  cursor = self.cursor
  stdscr.move(cursor[1], cursor[0])

 def setup_grid(self, dimensions, x_offset, y_offset):
  if dimensions < 0: raise InvalidDimensionException()
  self.dimensions = dimensions
  self.x_offset = x_offset
  self.y_offset = y_offset
  self.pos = [0] * dimensions
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
  elif key == curses.KEY_LEFT:
   return None
  elif key == curses.KEY_RIGHT:
   return None
  return key
 
 def input_turn(self, stdscr):
  stdscr.refresh()
  self.print_grid(stdscr)
  self.move_to_cursor(stdscr)
  if self.dimensions == 0:
   stdscr.getch()
   return
  key = None
  while not key or self.player_symbol == BLANK or self.grid_symbol != BLANK:
   key = stdscr.getch()
   key = self.apply_movement(key)
   self.move_to_cursor(stdscr)
   if self.player_symbol == BLANK and key != None and chr(key).isprintable():
    self.player_symbol = key
  self.grid_symbol = self.player_symbol
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
  center = self.center
  stdscr.addstr(center[1] - 1, center[0] - 1, '-' * 3)
  stdscr.addstr(center[1], center[0] - 1, f'|{self.grid[0]}|')
  stdscr.addstr(center[1] + 1, center[0] - 1, '-' * 3)

 def print_grid_1(self, stdscr):
  center = self.center
  for offset in self.grid:
   x = center[0]
   y = center[1] + 2 * offset
   stdscr.addstr(y - 1, x - 1, '-' * 3)
   stdscr.addstr(y, x - 1, f'|{self.grid[offset]}|')
   stdscr.addstr(y + 1, x - 1, '-' * 3)
  
def main(stdscr):
 game = ToeGame()
 game.setup_grid(1, 20, 10)
 victor = None
 while victor == None:
  stdscr.clear()
  stdscr.addstr(0, 0, f'Player: {game.player_turn}')
  game.input_turn(stdscr)
  victor = game.check_win()
 game.print_grid(stdscr)
 return victor

if __name__ == '__main__':
 victor = curses.wrapper(main)
 print(f'Game Over, Congratulations {victor}')
 


 
