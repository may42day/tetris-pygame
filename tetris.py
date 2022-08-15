import pygame
from pygame.locals import *
from random import choice
import sys

pygame.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption('Tetris')
fps = 60

# Colors
colors_dict = {
    'red' : (255, 50, 20),
    'orange' : (255, 150, 30),
    'yellow' : (255, 215, 0),
    'pink' : (220, 90, 200),
    'green' : (115, 200, 60),
    'blue' : (0, 65, 170),
    'purple' : (100, 50, 150),
    'field_border': (100, 115, 255),
    'field_background': (0, 0, 0),
    'text_start':(35, 255, 0),
    'text_button':(210, 0, 210),
    'text_lines':(255, 185, 40),
    'text_level':(255, 185, 40),
    'next_figure_border': (0, 0, 125),
    'game_over':(255, 255, 255),
    'game_over_background':(200,140,140,120),
}
# FONTS
fonts_dict = {
    'font' : pygame.font.Font(None, 40),
    'font2' : pygame.font.Font(None, 35),
    'font3' : pygame.font.Font(None, 25),
    'font4' : pygame.font.Font(None, 50),
    }

menu_dict = {
    'text1':{'text':'Press any button to start', 'color':colors_dict['text_start'], 'font':fonts_dict['font2'], 'x/y':(460, 90)},
    'text2':{'text':'use "LEFT ARROW" to move left', 'color':colors_dict['text_button'], 'font':fonts_dict['font3'], 'x/y':(460, 150)},
    'text3':{'text':'use "UP ARROW" to rotate figure', 'color':colors_dict['text_button'], 'font':fonts_dict['font3'], 'x/y':(460, 180)},
    'text4':{'text':'use "RIGHT ARROW" to move right', 'color':colors_dict['text_button'], 'font':fonts_dict['font3'], 'x/y':(460, 210)},
    'text5':{'text':'use F1 to restart', 'color':colors_dict['text_button'], 'font':fonts_dict['font3'], 'x/y':(460, 240)}, 
    'lines':{'text':'Lines: ', 'color':colors_dict['text_lines'], 'font':fonts_dict['font'], 'x/y':(460, 250)}, 
    'level':{'text':'Level: ', 'color':colors_dict['text_level'], 'font':fonts_dict['font'], 'x/y':(460, 290)}, 
    'Game_over':{'text':'Game over', 'color':colors_dict['game_over'], 'font':fonts_dict['font4'], 'x/y':(150, 300)}, 
}



class Game():
    is_game_started = False
    game_over = False 
    field = [0 if cell < 200 else 1 for cell in range(210)]
    cells_coordinates = []
    x_field = 90
    y_field = 50
    border_width = 10
    line_score = 0
    level = 1
    

    def draw_field(self):
        pygame.draw.rect(screen, colors_dict['field_border'], (self.x_field - self.border_width, self.y_field - self.border_width, 320, 620), self.border_width)
        pygame.draw.rect(screen, colors_dict['field_background'], (self.x_field, self.y_field, 300, 600))
        for cell in self.cells_coordinates[:-10]:
            x = 90 + cell[0] * 30 + 1
            y = 50 + cell[1] * 30 + 1
            color_key = self.field[cell[1] * 10 + cell[0]]
            if color_key:
                pygame.draw.rect(screen, colors_dict[color_key], (x, y, 28, 28))
        if self.is_game_started == True:
            self.draw_text(['lines'], f'{self.line_score}')
            self.draw_text(['level'], f'{self.level}')


    def draw_menu(self):
        self.draw_field()
        keys_list = ['text1', 'text2', 'text3', 'text4', 'text5']
        self.draw_text(keys_list)


    def draw_text(self, keys_list, add_text = ''):
        for key in keys_list:
            text = menu_dict[key]['font'].render(menu_dict[key]['text'] + add_text, True, menu_dict[key]['color'])
            screen.blit(text, menu_dict[key]['x/y'])        


    def update_field(self, color):
        for cell in figure.coordinates_list:
            self.field[cell[0] + (cell[1]-1) * 10] = color
            

    def restart_game(self):
        self.is_game_started = False
        self.field = [0 if cell < 200 else 1 for cell in range(210)]
        self.cells_coordinates = []
        figure.figure = []
        figure.next_figure = []
        figure.coordinates_list = []
        self.level = 1
        self.line_score = 0
        figure.x = 3
        figure.y = 0
        figure.speed = 0.1
        

    def check_for_filled_line(self):
        for row in range(20):
            counter = 0
            for column in self.field[row*10 : row*10 + 10]:
                if column:
                    counter +=1
            if counter == 10:
                self.line_score += 1
                for element in range(10):
                    self.field.pop(row * 10 + element)
                    self.field.insert(0, 0)
                              

    def get_all_object_coordinates(self):
        self.cells_coordinates = []
        for row in range(21):
            for column in range(10):
                if self.field[row*10 + column]:
                    self.cells_coordinates.append([column, row])
    

    def draw_game_over(self):
        screen2 = pygame.Surface((300,600), pygame.SRCALPHA)
        screen2.fill(colors_dict['game_over_background'])
        screen.blit(screen2, (90,50))
        self.draw_text(['Game_over'])


    def inrease_level(self):
        counter = game.line_score // 10
        if counter + 1 > self.level:
            self.level = counter + 1
            figure.speed = 0.1 + counter/ 100


class Figures():
    figure = []
    next_figure = []
    figures_dict = {
        'figure1':[
            [0, 0, 'red', 0,
            0, 0, 'red', 0,
            0, 0, 'red', 0,
            0, 0, 'red', 0],
            [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            'red', 'red', 'red', 'red']],
        'figure2':[
            [0, 'orange', 0, 0,
            0, 'orange', 'orange', 'orange',
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 'orange', 'orange', 0,
            0, 'orange', 0, 0,
            0, 'orange', 0, 0,
            0, 0, 0, 0],
            [0, 'orange', 'orange', 'orange',
            0, 0, 0, 'orange',
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 0, 'orange', 0,
            0, 0, 'orange', 0,
            0, 'orange', 'orange', 0,
            0, 0, 0, 0],
            ],
        'figure3':[
            [0, 0, 0, 'yellow',
            0, 'yellow', 'yellow', 'yellow',
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 'yellow', 0, 0,
            0, 'yellow', 0, 0,
            0, 'yellow', 'yellow', 0,
            0, 0, 0, 0], 
            [0, 'yellow', 'yellow', 'yellow',
            0, 'yellow', 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0], 
            [0, 'yellow', 'yellow', 0,
            0, 0, 'yellow', 0,
            0, 0, 'yellow', 0,
            0, 0, 0, 0]],
        'figure4':[
            [0, 'pink', 'pink', 0,
            0, 'pink', 'pink', 0,
            0, 0, 0, 0,
            0, 0, 0, 0]],
        'figure5':[
            [0, 0, 'green', 'green',
            0, 'green', 'green', 0,
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 0, 'green', 0,
            0, 0, 'green', 'green',
            0, 0, 0, 'green',
            0, 0, 0, 0]],
        'figure6':[
            [0, 0, 'blue', 0,
            0, 'blue', 'blue', 'blue',
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 0, 'blue', 0,
            0, 0, 'blue', 'blue',
            0, 0, 'blue', 0,
            0, 0, 0, 0], 
            [0, 'blue', 'blue', 'blue',
            0, 0, 'blue', 0,
            0, 0, 0, 0,
            0, 0, 0, 0], 
            [0, 0, 'blue', 0,
            0, 'blue', 'blue', 0,
            0, 0, 'blue', 0,
            0, 0, 0, 0]],
        'figure7':[
            ['purple', 'purple', 0, 0,
            0, 'purple', 'purple', 0,
            0, 0, 0, 0,
            0, 0, 0, 0],
            [0, 'purple', 0, 0,
            'purple', 'purple', 0, 0,
            'purple', 0, 0, 0,
            0, 0, 0, 0]],    
        }
    current_dict_key = ''
    next_dict_key = ''
    rotation_counter = 0
    coordinates_list = []
    speed = 0.1
    collision_for_next_figure = False

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
        self.collision_for_next_figure = True
        self.falling_collision()
        self.collision_for_next_figure = False
        

    def rotate_figure(self):
        if self.rotation_counter < len(self.figures_dict[self.current_dict_key]) - 1:
            check_rotation_counter = self.rotation_counter + 1
        else:
            check_rotation_counter = 0

        game.get_all_object_coordinates()
        self.coordinates_list = []
        figure_to_check = self.figures_dict[self.current_dict_key][check_rotation_counter]
        rotation_allowed = True
        for column in range(4):
            for row in range(4):
                if figure_to_check[row*4 + column] != 0:
                    if column + self.x < 0 or column + self.x > 9:
                        rotation_allowed = False
                        break

        if rotation_allowed:
            self.rotation_counter = check_rotation_counter
            self.figure = self.figures_dict[self.current_dict_key][self.rotation_counter]


    def draw_figure(self):
        for column in range(4):
            for row in range(4):
                if self.figure[row*4 + column] != 0:
                    x = self.x * 30 + game.x_field + 30 * column
                    y = self.y * 30 + game.y_field + 30 * row
                    color = self.figure[row*4 + column]
                    pygame.draw.rect(screen, colors_dict[color],(x, y, 30, 30))
        pygame.draw.rect(screen, colors_dict['next_figure_border'], (460, 60, 160, 160), 10)            
        for column in range(4):
            for row in range(4):
                if self.next_figure[row*4 + column] != 0:
                    x = 480  + 30 * column
                    y = 30 + 50 + 30 * row
                    color = self.next_figure[row*4 + column]
                    pygame.draw.rect(screen, colors_dict[color],(x, y, 30, 30))


    def falling_collision(self):
        game.get_all_object_coordinates()
        self.coordinates_list = []
        for column in range(4):
            for row in range(4):
                if self.figure[row*4 + column] != 0:
                    self.coordinates_list.append([column + self.x, row + round(self.y) + 1])
                    cell_color = self.figure[row*4 + column]
        for cell in self.coordinates_list:
            if cell in game.cells_coordinates:
                if self.collision_for_next_figure:
                    game.game_over = True
                    game.is_game_started = False
                else:
                    game.update_field(cell_color)
                    self.start_next_figure()
                break
        self.y += figure.speed


    def check_collision(self, direction):
        if direction == 'right':
            add_to_x = 1
        else:
            add_to_x = -1
        game.get_all_object_coordinates()
        self.coordinates_list = []
        for column in range(4):
            for row in range(4):
                if self.figure[row*4 + column] != 0:
                    self.coordinates_list.append([column + self.x + add_to_x, row + self.y])

        moving_allowed = True   
        for cell in self.coordinates_list:
            rounded_cell = [cell[0], round(cell[1])]
            print(rounded_cell)
            if rounded_cell in game.cells_coordinates: 
                moving_allowed = False
                break
                
        for cell in self.coordinates_list:
            if direction == 'right':
                if cell in game.cells_coordinates or cell[0] > 9:
                    moving_allowed = False
                    break
            else:
                if cell in game.cells_coordinates or cell[0] < 0:
                    moving_allowed = False
                    break

        if moving_allowed:
            if direction == 'right':
                self.x += 1
            else:
                self.x -= 1

game = Game()
figure = Figures(x = 3, y = 0)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and game.is_game_started == False and game.game_over == False and event.key != K_F1:
            game.is_game_started = True
            figure.generate_figure()
        elif event.type == pygame.KEYDOWN and event.key == K_F1:
            game.restart_game()
            game.game_over = False
        elif event.type == pygame.KEYDOWN and game.is_game_started == True:
            if event.key == K_RIGHT:
                # figure.move_to_right()
                figure.check_collision('right')
            elif event.key == K_LEFT:
                figure.check_collision('left')
            elif event.key == K_UP:
                figure.rotate_figure()

 
    screen.fill((10, 10, 10))
    if game.is_game_started == False:
        game.draw_menu()
    else:
        figure.falling_collision()
        game.check_for_filled_line()
        game.inrease_level()

    if game.game_over == True:
        game.draw_game_over()
    if game.is_game_started == True:
        game.draw_field()
        figure.draw_figure()

    pygame.display.flip()
    clock.tick(fps)