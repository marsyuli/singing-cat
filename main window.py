import pygame
import sys


pygame.init()
size = width, height = 800, 600

surface = pygame.display.set_mode(size)
pygame.display.set_caption('Singing Cat')
surface.fill('#ffc2cc')
font = pygame.font.Font('fonts/Cat.otf', 120)
text = font.render('Singing Cat', True, 'yellow')
surface.blit(text, ((width - text.get_rect()[2]) // 2, 50))
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
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        surface.blit(self.buttonSurface, self.buttonRect)


def func():
    print(':)')

def exit():
    pygame.quit()
    sys.exit()

Button(100, 230, 600, 80, 'Играть', func)
Button(100, 320, 600, 80, 'Правила', func)
Button(100, 410, 600, 80, 'Выйти', exit)

volume_button_image = pygame.image.load('images/volume.png')
volume_button_image = pygame.transform.scale(volume_button_image, (100, 100))
volume_button_rect = volume_button_image.get_rect()
surface.blit(volume_button_image, (690, 490))

mute_button_image = pygame.image.load('images/mute.png')
mute_button_image = pygame.transform.scale(mute_button_image, (100, 100))
mute_button_rect = mute_button_image.get_rect()

def volume_button_click():
    print(1)

pygame.mixer.music.load('music/Angel We Have Heard On High.mp3')
pygame.mixer.music.play()


pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if volume_button_rect.collidepoint(pygame.mouse.get_pos()):
                volume_button_click()
    for btn in buttons:
        btn.process()
    pygame.display.flip()