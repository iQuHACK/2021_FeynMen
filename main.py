import time
import pygame
from comparison import *
from vqeCalc2 import paulidecompos
import sympy as sp
import numpy as np
from PIL import Image, ImageFont, ImageDraw

display_width = 1000
display_height = 700

WHITE = (255, 255, 255)
RED = (255, 0, 0)
bg_location = 'gifs/photo-video-detail_0.png'

pygame.init()

# Profiles dictionary by list of properties
profiles_dict = {
    "[0,0,0,0]": {
        "Name": "Albert Einstein",
        "Age": 35,
        "Famous for": "Relativity",
        "Bio": "Relatively attractive."
    },
    "[0,0,0,1]": {
        "Name": "Marie Curie",
        "Age": 38,
        "Famous for": "Radiation",
        "Bio": "A radiant beauty."
    },
    "[0,0,1,0]": {
        "Name": "David Deutsch",
        "Age": 47,
        "Famous for": "Father of Quantum Computing",
        "Bio": "No discrete bits shall describe me."
    },
    "[0,0,1,1]": {
        "Name": "Euler",
        "Age": 28,
        "Famous for": "Everything Maths",
        "Bio": "M is for Maths which belongs to me."
    },
}

class Button(object):
    def __init__(self, text, color, x=None, y=None, **kwargs):
        self.surface = font.render(text, True, color)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['cenntered_y']:
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y

    def display(self):
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False


def starting_screen():
    screen.blit(bg, (0, 0))

    game_title = font.render('Let\'s FeynMen This!', True, RED)

    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 100))

    img = pygame.image.load('currentmatrix.png')
    img = pygame.transform.scale(img, (500, 200))
    screen.blit(img, ((display_width // 2 - img.get_width() // 2, 200)))


    play_button = Button('Play', RED, None, 500, centered_x=True)
    exit_button = Button('Exit', WHITE, None, 550, centered_x=True)

    play_button.display()
    exit_button.display()

    pygame.display.update()

    while True:

        if play_button.check_click(pygame.mouse.get_pos()):
            play_button = Button('Play', RED, None, 500, centered_x=True)
        else:
            play_button = Button('Play', WHITE, None, 500, centered_x=True)

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('Exit', RED, None, 550, centered_x=True)
        else:
            exit_button = Button('Exit', WHITE, None, 550, centered_x=True)

        play_button.display()
        exit_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if play_button.check_click(pygame.mouse.get_pos()):
                return True
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                return False
                break


def gate_choose():
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    circuit.draw('mpl', filename='gifs/currentcircuit.png')
    img = pygame.image.load('gifs/currentcircuit.png')
    img = pygame.transform.scale(img, (400, 200))
    screen.blit(img, (50, 20))

    img = pygame.image.load('currentmatrix.png')
    img = pygame.transform.scale(img, (500, 200))
    screen.blit(img, (500, 20))

    pygame.display.update()  # update the display
    game_title = font.render('Which gate would you like to choose?', True, RED)

    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 250))
    H_button = Button('H', WHITE, None, 350, centered_x=True)
    X_button = Button('X', WHITE, None, 400, centered_x=True)
    CNOT_button = Button('CNOT01', WHITE, None, 450, centered_x=True)
    DONE_button = Button('DONE', WHITE, None, 500, centered_x=True)

    H_button.display()
    X_button.display()
    CNOT_button.display()
    DONE_button.display()

    pygame.display.update()
    while True:

        if H_button.check_click(pygame.mouse.get_pos()):
            H_button = Button('H', RED, None, 350, centered_x=True)
        else:
            H_button = Button('H', WHITE, None, 350, centered_x=True)

        if X_button.check_click(pygame.mouse.get_pos()):
            X_button = Button('X', RED, None, 400, centered_x=True)
        else:
            X_button = Button('X', WHITE, None, 400, centered_x=True)

        if CNOT_button.check_click(pygame.mouse.get_pos()):
            CNOT_button = Button('CNOT01', RED, None, 450, centered_x=True)
        else:
            CNOT_button = Button('CNOT01', WHITE, None, 450, centered_x=True)

        if DONE_button.check_click(pygame.mouse.get_pos()):
            DONE_button = Button('DONE', RED, None, 500, centered_x=True)
        else:
            DONE_button = Button('DONE', WHITE, None, 500, centered_x=True)

        H_button.display()
        X_button.display()
        CNOT_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if H_button.check_click(pygame.mouse.get_pos()):
                return 'H'
                break
            if X_button.check_click(pygame.mouse.get_pos()):
                return "X"
                break
            if CNOT_button.check_click(pygame.mouse.get_pos()):
                return "C01"
                break
            if DONE_button.check_click(pygame.mouse.get_pos()):
                return "DONE"
                break


def qubit_choose():
    screen.blit(bg, (0, 0))
    game_title = font.render('Which qubit would you like to apply that gate on?', True, RED)

    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 250))
    zero_button = Button('0', WHITE, None, 350, centered_x=True)
    one_button = Button('1', WHITE, None, 400, centered_x=True)

    zero_button.display()
    one_button.display()

    pygame.display.update()
    while True:

        if zero_button.check_click(pygame.mouse.get_pos()):
            zero_button = Button('0', RED, None, 350, centered_x=True)
        else:
            zero_button = Button('0', WHITE, None, 350, centered_x=True)

        if one_button.check_click(pygame.mouse.get_pos()):
            one_button = Button('1', RED, None, 400, centered_x=True)
        else:
            one_button = Button('1', WHITE, None, 400, centered_x=True)

        zero_button.display()
        one_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if zero_button.check_click(pygame.mouse.get_pos()):
                return '0'
                break
            if one_button.check_click(pygame.mouse.get_pos()):
                return '1'
                break


def yes_screen():
    screen.blit(bg, (0, 0))
    game_title = font.render('You Got It! Congratulations!', True, RED)
    game_title2 = font.render('Now you successfully enter the field of ...', True, RED)

    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 150))
    screen.blit(game_title2, (display_width // 2 - game_title2.get_width() // 2, 250))

    continue_button = Button('CONTINUE', WHITE, None, 350, centered_x=True)
    exit_button = Button('EXIT', WHITE, None, 400, centered_x=True)

    continue_button.display()
    exit_button.display()

    pygame.display.update()
    while True:
        if continue_button.check_click(pygame.mouse.get_pos()):
            continue_button = Button('CONTINUE', RED, None, 350, centered_x=True)
        else:
            continue_button = Button('CONTINUE', WHITE, None, 350, centered_x=True)

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('EXIT', RED, None, 400, centered_x=True)
        else:
            exit_button = Button('EXIT', WHITE, None, 400, centered_x=True)

        continue_button.display()
        exit_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if continue_button.check_click(pygame.mouse.get_pos()):
                return 'continue'
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                return 'exit'
                break


def no_screen():
    screen.blit(bg, (0, 0))
    game_title = font.render('Unfortunately...', True, RED)
    game_title2 = font.render('Now you will enter the field of ...', True, RED)

    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 150))
    screen.blit(game_title2, (display_width // 2 - game_title2.get_width() // 2, 250))

    continue_button = Button('CONTINUE', WHITE, None, 350, centered_x=True)
    exit_button = Button('EXIT', WHITE, None, 400, centered_x=True)

    continue_button.display()
    exit_button.display()

    pygame.display.update()
    while True:

        if continue_button.check_click(pygame.mouse.get_pos()):
            continue_button = Button('CONTINUE', RED, None, 350, centered_x=True)
        else:
            continue_button = Button('CONTINUE', WHITE, None, 350, centered_x=True)

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('EXIT', RED, None, 400, centered_x=True)
        else:
            exit_button = Button('EXIT', WHITE, None, 400, centered_x=True)

        continue_button.display()
        exit_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        if pygame.mouse.get_pressed()[0]:
            if continue_button.check_click(pygame.mouse.get_pos()):
                return 'continue'
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                return 'exit'
                break

def match_screen():
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    #circuit.draw('mpl', filename='gifs/currentcircuit.png')
    img = pygame.image.load('profiles/einstein.jpg')
    img = pygame.transform.scale(img, (200, 300))
    screen.blit(img, (display_width // 2 - 200 // 2, 20))

    pygame.display.update()  # update the display
    game_title = font.render('It\'s a match', True, WHITE)

    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 400))
    DONE_button = Button('Found Love!', WHITE, 100, 500)
    REPEAT_button = Button('Match Again!', WHITE, 600, 500)

    DONE_button.display()
    REPEAT_button.display()

    pygame.display.update()
    while True:
        if DONE_button.check_click(pygame.mouse.get_pos()):
            DONE_button = Button('Found Love!', RED, 100, 500)
        else:
            DONE_button = Button('Found Love!', WHITE, 100, 500)
            
        if REPEAT_button.check_click(pygame.mouse.get_pos()):
            REPEAT_button = Button('Match Again!', RED, 600, 500)
        else:
            REPEAT_button = Button('Match Again!', WHITE, 600, 500)

        DONE_button.display()
        REPEAT_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
                
        if pygame.mouse.get_pressed()[0]:
            if REPEAT_button.check_click(pygame.mouse.get_pos()):
                return 'continue'
                break
            if DONE_button.check_click(pygame.mouse.get_pos()):
                return 'exit'
                break
                
    
while True:
    matriz, coeff = rando_hermitian()
    #matriz = sp.Matrix([[1, 0, 0, 0], [0, 0, -1, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
    #coeff = paulidecompos(matriz)
    #matriz = np.array(matriz).astype(np.float64)
    showMatrix= np.array_str(matriz[0]) + '\n' +np.array_str(matriz[1])+ '\n' +np.array_str(matriz[2])+ '\n' +np.array_str(matriz[3])
    im = Image.new("RGB", (270, 100), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = font = ImageFont.load_default()

    dr.text((20, 20), showMatrix, font=font, fill="#000000")
    im.save("currentmatrix.png")

    circuit = QuantumCircuit(2, 2)
    circuit.barrier()
    screen = pygame.display.set_mode((display_width, display_height))
    bg = pygame.image.load(bg_location)
    bg = pygame.transform.scale(bg, (1000, 700))
    font_addr = pygame.font.get_default_font()
    font = pygame.font.Font(font_addr, 36)
    fontMatrix = pygame.font.Font(font_addr, 18)

    playornot = starting_screen()
    time.sleep(0.5)
    if playornot:
        choice = []

        while True:
            gate_chosen = gate_choose()
            time.sleep(0.5)
            if gate_chosen == 'C01':
                choice.append(gate_chosen)
                circuit.cnot(0, 1)
                continue
            if gate_chosen[0] == 'H':
                qubit_chosen = qubit_choose()
                choice.append(gate_chosen + qubit_chosen)
                circuit.h(int(qubit_chosen))
                continue
            if gate_chosen[0] == 'X':
                qubit_chosen = qubit_choose()
                choice.append(gate_chosen + qubit_chosen)
                circuit.x(int(qubit_chosen))
                continue

            if gate_chosen == 'DONE':
                value = comparison(choice, matriz, coeff)
                if value:
                    print('Go to yes screen')
                    continueornot = match_screen()
                    time.sleep(0.5)
                    break
                else:
                    print('Go to no screen')
                    continueornot = match_screen()
                    time.sleep(0.5)
                    break
            time.sleep(0.5)
        if continueornot == 'exit':
            break
    else:
        break
