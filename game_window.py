import pygame
import random
import sys
import os


pygame.init()
size = width, height = 500, 600
falling_speed = 0.1

game_screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игровове окно')
game_screen.fill('#ffc2cc')


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


cat_right_image = pygame.transform.scale(load_image('cat_right.png'), (150, 150))
candy_image = pygame.transform.scale(load_image('candy.png'), (70, 70))
cat_mouth_image = pygame.transform.scale(load_image('cat_mouth.png'), (150, 150))
board_image = pygame.transform.scale(load_image('board.png'), (500, 100))
ice_cream_image = pygame.transform.scale(load_image('ice_cream.png'), (90, 90))
game_screen.blit(ice_cream_image, (0, 0))
game_screen.blit(candy_image, (100, 0))
game_screen.blit(board_image, (0, 405))
game_screen.blit(cat_mouth_image, (190, 300))
game_screen.blit(cat_right_image, (50, 305))
pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
