#!/usr/bin/python3
import curses
from random import shuffle

DEFAULT_SYMBOLS = 'XOLGBTIQ'
LINE = {-1: ' ', 0: ' ', 1: ' '}

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

 def setup_grid(self, dimensions, x_offset, y_offset):
  self.dimensions = dimensions
  self.x_offset = x_offset
  self.y_offset = y_offset
  self.pos = [0] * max(2, dimensions)
  if dimensions < 4:
   self.setup_players(dimensions)
   if dimensions == 0:
    self.grid = [' ']
   elif dimensions == 1:
    self.grid = LINE.copy()

 def setup_players(self, players):
  self.players = players
  self.symbols = list(' ' * players)
 
 def input_turn(self, stdscr):
  stdscr.refresh()
  self.print_grid(stdscr)
  stdscr.move(1 + self.y_offset + (self.pos[1] + 1) * 2, 
   1 + self.x_offset + (self.pos[0] + 1) * 2)
  if self.dimensions == 0:
   stdscr.getch()
   return
  key = None
  while not key:
   key = stdscr.getch()
   if self.symbols[self.player] == ' ' and chr(key).isprintable():
    self.symbols[self.player] = key
   if key == curses.KEY_LEFT:
    self.pos[0] = max(self.pos[0] - 1, -1)
    key = None
   elif key == curses.KEY_RIGHT:
    self.pos[0] = min(self.pos[0] + 1, 1)
    key = None
   elif self.dimensions > 1:
    if key == curses.KEY_UP:
     self.pos[1] = max(self.pos[1] - 1, -1)
     key = None
    elif key == curses.KEY_DOWN:
     self.pos[1] = min(self.pos[1] + 1, 1)
     key = None
   stdscr.move(1 + self.y_offset + self.pos[1] * 2, 
    1 + self.x_offset + self.pos[0] * 2)
  self.grid[self.pos[0]] = chr(key)

     

 def check_win(self):
  if self.dimensions == 0:
   return self.grid[0]
  elif self.dimensions == 1 and len(set(self.grid)) == 1:
   return self.grid[0]
  # TODO: Check for line through any dimensional pathway 
  return None
  
 def print_grid(self, stdscr):
  if self.dimensions == 0:
   self.print_grid_0(stdscr)
  if self.dimensions == 1:
   self.print_grid_1(stdscr)

 def print_grid_0(self, stdscr):
  stdscr.addstr(self.y_offset, self.x_offset, '_' * 3)
  stdscr.addstr(1 + self.y_offset, self.x_offset, f'|{self.grid[0]}|')
  stdscr.addstr(2 + self.y_offset, self.x_offset, '-' * 3)

 def print_grid_1(self, stdscr):
  stdscr.addstr(self.y_offset, self.x_offset, '_' * (1 + 2 * 3))
  stdscr.addstr(1 + self.y_offset, self.x_offset,
   '|' + ''.join([f'{self.grid[i]}|' for i in range(-1,2)]))
  stdscr.addstr(2 + self.y_offset, self.x_offset, '-' * (1 + 2 * 3))
  
def main(stdscr):
 game = ToeGame()
 game.setup_grid(1, 2, 1)
 victor = None
 while victor == None:
  stdscr.clear()
  game.input_turn(stdscr)
  victor = game.check_win()
 game.print_grid(stdscr)
 return victor

if __name__ == '__main__':
 victor = curses.wrapper(main)
 print(f'Game Over, Congratulations {victor}')
 


 
