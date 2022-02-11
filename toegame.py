#!/usr/bin/python3

from random import choice
from math import floor
import curses

DEFAULT_SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
  offset = 1
  cursor_dim = 0
  for d in range(self.dimensions):
   offset = 2 * offset
   cursor_dim = (cursor_dim + 1) % len(cursor)
   cursor[cursor_dim] = cursor[cursor_dim] + offset * self.pos[d]
  return cursor

 @property
 def player_turn(self):
  if self.dimensions == 0: return BLANK
  turn = self.player_symbol
  if turn == BLANK: return 'NEW'
  return turn

 @property
 def player_symbol(self):
  return self.symbols[self.player]

 @player_symbol.setter
 def player_symbol(self, value):
  symbol = chr(value)
  if symbol == BLANK or not symbol.isprintable():
   symbol = choice(DEFAULT_SYMBOLS)
  while symbol in self.symbols:
   symbol = choice(DEFAULT_SYMBOLS)
  self.symbols[self.player] = symbol

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
  self.setup_players(dimensions)
  if dimensions == 0:
   self.grid = [BLANK]
   return
  self.grid = LINE.copy()
  for d in range(2, dimensions + 1):
   self.grid = {-1: self.grid.copy(),
                 0: self.grid.copy(),
                 1: self.grid.copy()}

 def setup_players(self, players):
  self.players = players
  self.symbols = list(BLANK * players)

 def apply_input(self, key):
  if key == curses.KEY_UP:
   self.apply_movement(0, -1)
   return None
  elif key == curses.KEY_DOWN:
   self.apply_movement(0, 1)
   return None
  elif key == curses.KEY_LEFT:
   self.apply_movement(1, -1)
   return None
  elif key == curses.KEY_RIGHT:
   self.apply_movement(1, -1)
   return None
  return key
  
 def apply_movement(self, dimension, direction):
  while dimension < len(self.pos):
   self.pos[dimension] = self.pos[dimension] + direction
   if abs(self.pos[dimension]) <= 1:
    return
   else:
    self.pos[dimension] = max(-1, min(self.pos[dimension], 1))
   dimension = dimension + 2
 
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
   key = self.apply_input(key)
   self.move_to_cursor(stdscr)
   if self.player_symbol == BLANK and key != None:
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
   return
  if self.dimensions == 1:
   self.print_grid_1(stdscr)
   return
  if self.dimensions == 2:
   self.print_grid_2(stdscr)
   return

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
   cell = f'| {self.grid[offset]} |'
   stdscr.addstr(y - 1, x - 1, '-' * 3)
   stdscr.addstr(y, x - floor(len(cell) / 2), cell)
   stdscr.addstr(y + 1, x - 1, '-' * 3)

 def print_grid_2(self, stdscr):
  pass
  
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
