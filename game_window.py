import pygame
import sys
import os


pygame.init()
size = width, height = 500, 600
falling_speed = 0.1

game_screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игровове окно')
game_screen.fill('#EFCDD6')
all_sprites = pygame.sprite.Group()
cat_group = pygame.sprite.Group()
board_group = pygame.sprite.Group()


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


class Board(pygame.sprite.Sprite):
    board_image = pygame.transform.scale(load_image('board.png'), (500, 100))

    def __init__(self):
        super().__init__(all_sprites, board_group)
        self.image = Board.board_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 405


class Cat(pygame.sprite.Sprite):
    cat_right_image = pygame.transform.scale(load_image('cat_right.png'), (150, 150))

    def __init__(self):
        super().__init__(all_sprites, cat_group)
        self.image = Cat.cat_right_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 305

    def update(self, event):
        if event.key == pygame.K_LEFT:
            self.rect.x -= 10
        if event.key == pygame.K_RIGHT:
            self.rect.x += 10


board = Board()
cat = Cat()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            cat_group.update(event)
    game_screen.fill('#EFCDD6')
    all_sprites.draw(game_screen)
    pygame.display.flip()
pygame.quit()
