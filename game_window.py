import pygame
import sys
import os
import random
from Sprite import board_group, cat_group, candy_group, all_sprites, ice_cream_group


pygame.init()
size = width, height = 500, 600
font_name = pygame.font.match_font('arial')

game_screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игровове окно')
game_screen.fill('#EFCDD6')

pygame.mixer.music.load('music/Billie_Eilish-What_Was_I_Made_For.mp3')


def load_image(name, colorkey=None): # функция для загрузки изображений
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


def game_over_screen():
    fon_game_over_image = pygame.transform.scale(load_image('fon.jpg'), (500, 600))
    game_screen.blit(fon_game_over_image, (0, 0))
    draw_text(game_screen, 'Игра окончена', 36, width / 2, 50, 'black')
    draw_text(game_screen, f'Ваш счет: {quantity}', 24, width / 2, 95, '#91231D')
    draw_text(game_screen, f'Ваш лучший результат:', 24, width / 2, 130, '#91231D')


def draw_text(surf, text, size_text, x, y, color):
    font = pygame.font.Font(font_name, size_text)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Board(pygame.sprite.Sprite):
    # Создание доски на которой будет находиться кот
    board_image = pygame.transform.scale(load_image('board.png'), (500, 100))

    def __init__(self):
        super().__init__(all_sprites, board_group)
        self.image = Board.board_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 405


class Cat(pygame.sprite.Sprite): # Создание кота
    # Добавление картинок кота
    cat_right_image = pygame.transform.scale(load_image('cat_right.png'), (150, 150))
    cat_mouth_right = pygame.transform.scale(load_image('cat_mouth_right.png'), (150, 150))
    cat_left_image = pygame.transform.scale(load_image('cat_left.png'), (150, 150))
    cat_mouth_image = pygame.transform.scale(load_image('cat_mouth.png'), (145, 145))

    def __init__(self):
        super().__init__(all_sprites, cat_group)
        self.image = Cat.cat_right_image
        self.rect = self.image.get_rect()
        self.rect.x = 170
        self.rect.y = 305

    def update(self, event):
        # Передвижение кота + изменение картинки
        if event.key == pygame.K_LEFT:
            if self.rect.x > 15:
                self.rect.x -= 8
                self.image = Cat.cat_right_image
        if event.key == pygame.K_RIGHT:
            if self.rect.x < 350:
                self.rect.x += 8
                self.image = Cat.cat_left_image


class Ice_cream(pygame.sprite.Sprite): # Создание мороженого
    # Добавление картинки мороженого
    ice_cream_image = pygame.transform.scale(load_image('ice_cream.png'), (90, 90))

    def __init__(self):
        super().__init__(all_sprites, ice_cream_group)
        self.image = Ice_cream.ice_cream_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = random.randint(15, 370), -80

    def update(self): # Передвижение мороженого + удаление мороженого + изменение кота
        global quantity
        if not pygame.sprite.collide_mask(self, cat):
            self.rect = self.rect.move(0, 1)
            if self.rect.y == 480:
                self.kill()
                quantity -= 10
        else:
            if cat.image == cat.cat_right_image:
                cat.image = cat.cat_mouth_right
            elif cat.image == cat.cat_left_image:
                cat.image = cat.cat_mouth_image
            quantity += 10
            self.kill()


class Candy(pygame.sprite.Sprite): # Создание конфеты
    # Добавление конфеты
    candy_image = pygame.transform.scale(load_image('candy.png'), (70, 70))

    def __init__(self):
        super().__init__(all_sprites, candy_group)
        self.image = Candy.candy_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = random.randint(15, 370), -80

    def update(self): # Передвижение конфеты + удаление конфеты + изменение кота
        global quantity
        if not pygame.sprite.collide_mask(self, cat):
            self.rect = self.rect.move(0, 1)
            if self.rect.y == 480:
                self.kill()
                quantity -= 15
        else:
            if cat.image == cat.cat_right_image:
                cat.image = cat.cat_mouth_right
            elif cat.image == cat.cat_left_image:
                cat.image = cat.cat_mouth_image
            quantity += 15
            self.kill()


def pause(): # Функция паузы игры
    paused = True
    while paused:
        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    paused = False
                    pygame.mixer.music.unpause()
        pygame.display.update()
        clock.tick(15)


board = Board()
cat = Cat()
quantity = 0
clock = pygame.time.Clock()


def game():
    global board, cat, quantity, clock
    pygame.mixer.music.play()
    pygame.time.set_timer(pygame.USEREVENT, 2000)
    fon = pygame.transform.scale(load_image('game_fon.jpg'), (500, 600))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                cat_group.update(event)
            if event.type == pygame.USEREVENT:
                if pygame.mixer.music.get_busy():
                    candy_or_ice_cream = random.choice(['ice_cream', 'candy'])
                    if candy_or_ice_cream == 'ice_cream':
                        Ice_cream()
                    else:
                        Candy()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    pause()
        game_screen.blit(fon, (0, 0))
        all_sprites.draw(game_screen)
        candy_group.update()
        ice_cream_group.update()
        draw_text(game_screen, str(quantity), 36, width / 2, 10, 'black')
        if pygame.mixer.music.get_busy() == False:
            game_over_screen()
        clock.tick(60)
        pygame.display.flip()
