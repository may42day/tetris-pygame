import pygame
from pygame.locals import *
from random import choice
import sys

pygame.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption('Tetris')

cell_size = 30
# Colors
color1 = (97, 113, 255)
color2 = (0, 0, 0)
red = (255, 50, 20)
orange = (255, 150, 30)
yellow = (255, 215, 0)
pink = (219, 88, 197)
green = (115, 200, 60)
blue = (0, 65, 170)
purple = (100, 50, 150)

class Game():
    is_game_started = False
    field = [0 if cell < 200 else 1 for cell in range(210)]
    x_field = 90
    y_field = 50
    border_width = 10
    cells_coordinates = []

    def draw_field(self):
        pygame.draw.rect(screen, color1, (self.x_field - self.border_width, self.y_field - self.border_width, 320, 620), self.border_width)
        pygame.draw.rect(screen, color2, (self.x_field, self.y_field, 300, 600))
        for cell in self.cells_coordinates[:-10]:
            x = 90 + cell[0] * 30 + 1
            y = 50 + cell[1] * 30 + 1
            pygame.draw.rect(screen, (155, 244, 22), (x, y, 28, 28))

    def update_field(self):
        for cell in figure.coordinates_list:
            self.field[cell[0] + (cell[1]-1) * 10] = 1
            

    def restart_game(self):
        self.is_game_started = False
        self.field = [0 if cell < 200 else 1 for cell in range(210)]
        self.cells_coordinates = []
        figure.figure = []
        figure.next_figure = []
        figure.coordinates_list = []
        figure.x = 3
        figure.y = 0

    def check_for_filled_line(self):
        for row in range(20):
            counter = 0
            for column in self.field[row*10 : row*10 + 10]:
                if column:
                    counter +=1
            if counter == 10:
                #add_score
                for element in range(10):
                    self.field.pop(row * 10 + element)
                    self.field.insert(0, 0)
                              

    def get_all_object_coordinates(self):
        self.cells_coordinates = []
        for row in range(21):
            for column in range(10):
                if self.field[row*10 + column]:
                    self.cells_coordinates.append([column, row])


class Figures():
    figure = []
    next_figure = []
    figures_dict = {
        'figure1':[
            [0, 0, 1, 0,
            0, 0, 1, 0,
            0, 0, 1, 0,
            0, 0, 1, 0],
            [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            1, 1, 1, 1]],
        'figure2':[
            [0, 1, 0, 0,
            0, 1, 1, 1,
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 1, 1, 0,
            0, 1, 0, 0,
            0, 1, 0, 0,
            0, 0, 0, 0],
            [0, 1, 1, 1,
            0, 0, 0, 1,
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 0, 1, 0,
            0, 0, 1, 0,
            0, 1, 1, 0,
            0, 0, 0, 0],
            ],
        'figure3':[
            [0, 0, 0, 1,
            0, 1, 1, 1,
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 1, 0, 0,
            0, 1, 0, 0,
            0, 1, 1, 0,
            0, 0, 0, 0], 
            [0, 1, 1, 1,
            0, 1, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0], 
            [0, 1, 1, 0,
            0, 0, 1, 0,
            0, 0, 1, 0,
            0, 0, 0, 0],],
        'figure4':[
            [0, 1, 1, 0,
            0, 1, 1, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]],
        'figure5':[
            [0, 0, 1, 1,
            0, 1, 1, 0,
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 0, 1, 0,
            0, 0, 1, 1,
            0, 0, 0, 1,
            0, 0, 0, 0]],
        'figure6':[
            [0, 0, 1, 0,
            0, 1, 1, 1,
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 0, 1, 0,
            0, 0, 1, 1,
            0, 0, 1, 0,
            0, 0, 0, 0], 
            [0, 1, 1, 1,
            0, 0, 1, 0,
            0, 0, 0, 0,
            0, 0, 0, 0], 
            [0, 0, 1, 0,
            0, 1, 1, 0,
            0, 0, 1, 0,
            0, 0, 0, 0]],
        'figure7':[
            [1, 1, 0, 0,
            0, 1, 1, 0,
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 1, 0, 0,
            1, 1, 0, 0,
            1, 0, 0, 0,
            0, 0, 0, 0]],    
        }
    current_dict_key = ''
    next_dict_key = ''
    rotation_counter = 0
    coordinates_list = []

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def generate_figure(self):
        if len(self.figure) == 0:
            self.current_dict_key = choice(list(self.figures_dict.keys()))
            self.figure = self.figures_dict[self.current_dict_key][0]
        self.next_dict_key = choice(list(self.figures_dict.keys()))   
        self.next_figure = self.figures_dict[self.next_dict_key][0]

    def start_next_figure(self):
        self.figure = self.next_figure
        self.rotation_counter = 0
        self.current_dict_key = self.next_dict_key
        self.generate_figure()
        self.x = 3
        self.y = 0
        

    def rotate_figure(self):
        print(self.current_dict_key)
        if self.rotation_counter < len(self.figures_dict[self.current_dict_key]) - 1:
            self.rotation_counter += 1
        else:
            self.rotation_counter = 0
        self.figure = self.figures_dict[self.current_dict_key][self.rotation_counter]

    def draw_figure(self):

        for column in range(4):
            for row in range(4):
                if self.figure[row*4 + column] != 0:
                    x = self.x * 30 + game.x_field + 30 * column
                    y = self.y * 30 + game.y_field + 30 * row
                    pygame.draw.rect(screen, (12, 113, 255),(x, y, 30, 30))

    def falling_collision(self):
        game.get_all_object_coordinates()
        self.coordinates_list = []
        for column in range(4):
            for row in range(4):
                if self.figure[row*4 + column] != 0:
                    self.coordinates_list.append([column + self.x, row + self.y + 1])
        for cell in self.coordinates_list:
            if cell in game.cells_coordinates:
                game.update_field()
                self.start_next_figure()
                print('COL', self.coordinates_list)
                break
        self.y += 1
    
    def move_to_left(self):
        game.get_all_object_coordinates()
        self.coordinates_list = []
        for column in range(4):
            for row in range(4):
                if self.figure[row*4 + column] != 0:
                    self.coordinates_list.append([column + self.x - 1, row + self.y])
        
        moving_allowed = True    
        for cell in self.coordinates_list:
            if cell in game.cells_coordinates or cell[0] < 0:
                moving_allowed = False
                break

        if moving_allowed:
            self.x -= 1


    def move_to_right(self):
        game.get_all_object_coordinates()
        self.coordinates_list = []
        for column in range(4):
            for row in range(4):
                if self.figure[row*4 + column] != 0:
                    self.coordinates_list.append([column + self.x + 1, row + self.y])
        
        moving_allowed = True    
        for cell in self.coordinates_list:
            if cell in game.cells_coordinates or cell[0] > 9:
                moving_allowed = False
                break

        if moving_allowed:
            self.x += 1



game = Game()
figure = Figures(x = 3, y = 0)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.is_game_started = True
            figure.generate_figure()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_F1:
                game.restart_game()
            elif event.key == K_RIGHT:
                figure.move_to_right()
            elif event.key == K_LEFT:
                figure.move_to_left()
            elif event.key == K_UP:
                figure.rotate_figure()

    if game.is_game_started != True:
        pass
    else:
        figure.falling_collision()
        game.check_for_filled_line()

    #drawing
        screen.fill((10, 10, 10))
        game.draw_field()
        figure.draw_figure()
    pygame.display.flip()
    clock.tick(8)