import pygame
import sys
import os
from registration_window import registration
from sound import background_sound
from leaderboard import leaderboard


pygame.init()
size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(size)

background_sound.play()

buttons = []
buttonFont = pygame.font.Font('fonts/Collect Em All BB.ttf', 28)


class Button:
    def __init__(self, x, y, width, height, buttonText='', function=None, onePress=False):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.buttonText = buttonText
        self.function = function
        self.onePress = onePress
        self.alreadyPress = False
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#876c99',
            'pressed': '#333333'
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = buttonFont.render(buttonText, True, (20, 20, 20))
        buttons.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.function()
                elif not self.alreadyPress:

                    self.function()
                    self.alreadyPress = True
            else:
                self.alreadyPress = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2])
        screen.blit(self.buttonSurface, self.buttonRect)


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def open_registration_window():
    registration()


def open_leaderboard():
    leaderboard()


def terminate():
    pygame.quit()
    sys.exit()


Button(470, 260, 300, 70, 'Играть', open_registration_window)
Button(470, 340, 300, 70, 'Таблица лидеров', open_leaderboard)
Button(470, 420, 300, 70, 'Выйти', terminate)


def start_screen():
    heading = 'Singing Cat'
    fon = pygame.transform.scale(pygame.image.load('pictures/new_fon.gif'), (800, 800))
    screen.blit(fon, (0, -150))
    font = pygame.font.Font('fonts/Cat.otf', 120)
    heading_render = font.render(heading, 1, pygame.Color('white'))
    heading_rect = heading_render.get_rect()
    heading_rect.top = 40
    heading_rect.x = (screen_width - heading_rect[2]) / 2
    screen.blit(heading_render, heading_rect)
    while True:
        for btn in buttons:
            btn.process()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
pygame.quit()