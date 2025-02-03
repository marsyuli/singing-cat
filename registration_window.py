import pygame
import sys
import sqlite3


pygame.init()
size = screen_width, screem_height = 800, 600
screen = pygame.display.set_mode(size)

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
            'hover': '#666666',
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


def terminate():
    pygame.quit()
    sys.exit()


Button(225, 400, 350, 70, 'Войти', terminate)
Button(225, 480, 350, 70, 'Зарегистрироваться', terminate)


def registration():
    heading = 'Войдите или зарегистрируйтесь'
    fon = pygame.transform.scale(pygame.image.load('pictures/fon.gif'), size)
    screen.blit(fon, (0, 0))
    heading_font = pygame.font.Font('fonts/Collect Em All BB.ttf', 42)
    heading_render = heading_font.render(heading, 1, pygame.Color('white'))
    heading_rect = heading_render.get_rect()
    heading_rect.top = 40
    heading_rect.x = (screen_width - heading_rect[2]) / 2
    screen.blit(heading_render, heading_rect)
    text_font = pygame.font.Font('fonts/Collect Em All BB.ttf', 32)
    text = ['Имя пользователя:', 'Пароль:']
    for i in range(len(text)):
        text_render = text_font.render(text[i], 1, pygame.Color('white'))
        shade_render = text_font.render(text[i], 1, pygame.Color('black'))
        text_rect = text_render.get_rect()
        shade_rect = shade_render.get_rect()
        text_rect.top, shade_rect.top = 200 + (i * 70), 200 + (70 * i) + 2.5
        text_rect.x, shade_rect.x = 100, 102.5
        screen.blit(shade_render, shade_rect)
        screen.blit(text_render, text_rect)
    username, password = '', ''
    username_rect, password_rect = pygame.Rect(400, 207, 200, 30), pygame.Rect(220, 277, 200, 30)
    normal_color = pygame.Color('white')
    hover_color = pygame.Color('lightgrey')
    username_color, password_color = hover_color, hover_color
    username_flag, password_flag = False, False
    while True:
        for btn in buttons:
            btn.process()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_rect.collidepoint(event.pos):
                    username_flag = True
                else:
                    username_flag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if password_rect.collidepoint(event.pos):
                    password_flag = True
                else:
                    password_flag = False
            if event.type == pygame.KEYDOWN and username_flag:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            if event.type == pygame.KEYDOWN and password_flag:
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    username += '*'
        if username_flag:
            username_color = normal_color
        elif password_flag:
            password_color = normal_color
        else:
            username_color, password_color = hover_color, hover_color
        pygame.draw.rect(screen, username_color, username_rect)
        text_surface = text_font.render(username, True, (0, 0, 0))
        screen.blit(text_surface, (username_rect.x + 5, username_rect.y + 5))
        username_rect.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(screen, password_color, password_rect)
        text_surface1 = text_font.render(password, True, (0, 0, 0))
        screen.blit(text_surface1, (password_rect.x + 5, password_rect.y + 5))
        password_rect.w = max(100, text_surface1.get_width() + 10)
        pygame.display.flip()


registration()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
pygame.quit()