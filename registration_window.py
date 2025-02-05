import pygame
import sys
import sqlite3
from game_window import game
from sound import background_sound


pygame.init()
size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(size)

buttons = []
buttonFont = pygame.font.Font('fonts/Collect Em All BB.ttf', 28)


class Button: # Класс для создания кнопок
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


flag = False

def terminate(): # Закрытие окна
    pygame.quit()
    sys.exit()


def start_game(): # Начало игры
    global flag
    flag = True
    if flag:
        background_sound.set_volume(0)
        pygame.display.set_mode((500, 600))
        game()

def correct_name(username): # Проверка на существование пользователя
    global flag
    users = dict()
    max_id = 0
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()
    all_users = cur.execute("""SELECT * FROM all_users""").fetchall()
    for user in all_users:
        users[user[1]] = user[2]
        if user[0] > max_id:
            max_id = user[0]
    # if username not in list(users.keys()):
        # cur.execute(f'INSERT INTO all_users (id, username, score) VALUES ({max_id + 1}, {username}, 0)')
    # con.commit()
    # con.close()


normal_color = pygame.Color('white')
hover_color = pygame.Color('lightgrey')
text_font = pygame.font.Font('fonts/Collect Em All BB.ttf', 32)


Button(225, 400, 350, 70, 'Продолжить', start_game)


def registration(): # Окно регистрации
    global normal_color, hover_color, text_font
    heading = 'Введите имя пользователя'
    fon = pygame.transform.scale(pygame.image.load('pictures/new_fon.gif'), (800, 800))
    screen.blit(fon, (0, -150))
    heading_font = pygame.font.Font('fonts/Collect Em All BB.ttf', 42)
    heading_render = heading_font.render(heading, 1, pygame.Color('white'))
    heading_rect = heading_render.get_rect()
    heading_rect.top = 40
    heading_rect.x = (screen_width - heading_rect[2]) / 2
    screen.blit(heading_render, heading_rect)

    text = 'Имя пользователя:'
    text_render = text_font.render(text, 1, pygame.Color('white'))
    shade_render = text_font.render(text, 1, pygame.Color('black'))
    text_rect = text_render.get_rect()
    shade_rect = shade_render.get_rect()
    text_rect.top, shade_rect.top = 220, 222.5
    text_rect.x, shade_rect.x = 150, 152.5
    screen.blit(shade_render, shade_rect)
    screen.blit(text_render, text_rect)
    username = ''
    username_rect = pygame.Rect(450, 227, 200, 30)
    username_color = hover_color
    username_flag = False
    while True:
        for btn in buttons:
            btn.process()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_rect.collidepoint(event.pos):
                    username_flag = True
                else:
                    username_flag = False
            if event.type == pygame.KEYDOWN and username_flag:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
        if username_flag:
            username_color = normal_color
        else:
            username_color = hover_color
        pygame.draw.rect(screen, username_color, username_rect)
        text_surface = text_font.render(username, True, (0, 0, 0))
        screen.blit(text_surface, (username_rect.x + 5, username_rect.y - 3.5))
        username_rect.w = max(100, text_surface.get_width() + 10)
        if username != '':
            correct_name(username)
        pygame.display.flip()