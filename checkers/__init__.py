import pygame
from glob import glob

width = 500
height = 500
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
pygame.display.set_caption("PyCheckers")

from checkers.Board import Board
from checkers.GameInterface import GameInterface
from checkers.Button import Button
from checkers.TextButton import TextButton
from checkers.MenuButton import MenuButton
from checkers.surfaces import font, small_font, smaller_font
from checkers.Menu import Menu
from checkers.Game import Game

about_text = "Checkers, or Draughts, is a two player board game, consisted of 24 discs called knights, 12 for each player, pieces can move diagonaly one square at a time, if an enemy piece is one square of distance, it can capture the piece by jumping over if the next square is empty, you're even allowed..."

about_text_2 = "...To do multiple captures at once. If a piece reaches the end of their side of the board, they turn into queens, in this version of checkers, queens are able to go backwards, a player loses if he's not allowed to make a move, or have no pieces left..."

about_text_3 = "...Checkers has differents rules in different places, some differences compared to other versions of the game are: the board size is 8x8, captures are not obligatory, a queen can only move one square at a time. This game's version is not very complex, and doesn't have a lot of nuanced rules.."

comming_soon_text = "The one player mode isn't available yet. Stay tuned for more! "
