import pygame
import sys
import os


pygame.init()
size = surface_width, surface_height = 800, 600

surface = pygame.display.set_mode(size)
pygame.display.set_caption('Singing Cat')
surface.fill('#ffc2cc')
font = pygame.font.Font('fonts/Cat.otf', 120)
text = font.render('Singing Cat', True, 'yellow')
surface.blit(text, ((surface_width - text.get_rect()[2]) // 2, 50))

pygame.mixer.music.load('music/Angel We Have Heard On High.mp3')
pygame.mixer.music.play()

buttonFont = pygame.font.Font('fonts/Collect Em All BB.ttf', 28)
buttons = []
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
        surface.blit(self.buttonSurface, self.buttonRect)


def func():
    print(':)')

def exit():
    pygame.quit()
    sys.exit()

Button(100, 230, 600, 80, 'Играть', func)
Button(100, 320, 600, 80, 'Правила', func)
Button(100, 410, 600, 80, 'Выйти', exit)


def image_load(name, colorkey=None):
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



class MusicButton:
    def __init__(self, x, y, default_image, clicked_image):
        self.default_image = pygame.transform.scale(pygame.image.load(default_image), (100, 100))
        self.clicked_image = pygame.transform.scale(pygame.image.load(clicked_image), (100, 100))
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                self.image = self.clicked_image
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            self.image = self.default_image
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


MusicButton(690, 450, 'pictures/volume.png', 'pictures/mute.png')
pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for btn in buttons:
        btn.process()
    pygame.display.flip()