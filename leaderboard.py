import pygame
import sys
from sound import background_sound
import sqlite3

pygame.init()
size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(size)


def terminate():
    pygame.init()
    sys.exit()


def leaderboard():
    heading = 'Таблица лидеров'
    fon = pygame.transform.scale(pygame.image.load('pictures/new_fon.gif'), (800, 800))
    screen.blit(fon, (0, -150))
    heading_font = pygame.font.Font('fonts/Collect Em All BB.ttf', 42)
    heading_render = heading_font.render(heading, 1, pygame.Color('white'))
    heading_rect = heading_render.get_rect()
    heading_rect.top = 40
    heading_rect.x = (screen_width - heading_rect[2]) / 2
    screen.blit(heading_render, heading_rect)
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM all_users""").fetchall()

    headings = ['Имя пользователя', 'Количество очков']
    font = pygame.font.Font('fonts/Collect Em All BB.ttf', 24)
    for i in range(len(headings)):
        headings_render = font.render(headings[i], 1, pygame.Color('white'))
        headings_rect = headings_render.get_rect()
        headings_rect.top, headings_rect.x = 130, 200 + (i * 300)
        screen.blit(headings_render, headings_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
