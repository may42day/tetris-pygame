import pygame
from random import choice
import sys

pygame.init()


screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption('Tetris')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()