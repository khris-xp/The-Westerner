import pygame
import sys
from settings import *


def draw_text(text, color, size, screen, pos):
    global screen_width, screen_height
    font = pygame.font.Font('../font/subatomic.ttf', size)
    textobj = font.render(text, False, color)
    textrect = textobj.get_rect(center=pos)
    screen.blit(textobj, textrect)


def gameOver(screen, clock, score):
    font = pygame.font.Font('../font/subatomic.ttf', 20)
    user_ip = ''
    text_box = pygame.Rect(
        (WINDOW_WIDTH/2 - 350/2, WINDOW_HEIGHT/2 + 60), (350, 50))
    active = False
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if text_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if menu_button.collidepoint((mx, my)):
                    file = open('score.txt', 'a')
                    file.write(f'{user_ip}, {score}\n')
                    file.flush()
                    file.close()
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_ip = user_ip[:-1]
                    else:
                        user_ip += event.unicode
                        if surf.get_width() > text_box.w - 20:
                            user_ip = user_ip[:-1]

        background_image = pygame.image.load('../graphics/other/Background.png')
        screen.blit(background_image, (0, 0))
        draw_text('GAMEOVER', ('#F7EDDC'), 100, screen,
                  (WINDOW_WIDTH / 2 + 3, 140 + 3))
        draw_text('GAMEOVER', ('#FF4133'), 100,
                  screen, (WINDOW_WIDTH / 2, 140))

        draw_text(f'score : {score}', ('#996633'), 50,
                  screen, (WINDOW_WIDTH/2 + 3, 195 + 33))
        draw_text(f'score : {score}', ('#F7EDDC'),
                  50, screen, (WINDOW_WIDTH/2, 195 + 30))

        draw_text('TYPE YOUR NAME', ('#996633'), 50,
                  screen, (WINDOW_WIDTH/2 + 3, 300 + 3))
        draw_text('TYPE YOUR NAME', ('#F7EDDC'),
                  50, screen, (WINDOW_WIDTH/2, 300))

        menu_button = pygame.Rect((820, 550), (150, 50))
        pygame.draw.rect(screen, ('#61452C'), menu_button)
        draw_text('QUIT', ('#FFF4EB'), 50, screen, (900, 580))

        if active:
            color = pygame.Color('#FFF1E6')
        else:
            color = pygame.Color('#AE7A4D')

        pygame.draw.rect(screen, color, text_box)
        surf = font.render(user_ip, True, '#7D5536')
        screen.blit(surf, (text_box.x + 5, text_box.y + 5))

        pygame.display.update()
        clock.tick(60)
