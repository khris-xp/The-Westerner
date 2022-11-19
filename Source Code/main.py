import pygame
import sys
from gamerun import Gamerun
from settings import *

pygame.init()
pygame.display.set_caption('The Westerner')
clock = pygame.time.Clock()
gamerun = Gamerun(screen,clock)
bg_music = pygame.mixer.Sound('../Infographic/sound/main.mp3')
bg_music.play(loops=-1)

screen_width = WINDOW_WIDTH
screen_height = WINDOW_HEIGHT

def ranking():
    global scores, rankscores, show
    if show != 1:
        scores = []
        rankscores = []
        with open('score.txt') as file:
            for line in file:
                name, score = line.split(',')
                score = int(score)
                scores.append((name, score))
            scores.sort(key=lambda s: s[1])
            scores.reverse()
            for num in range(0, 5):
                rankscores.insert(num,scores[num])
            file.flush()
            show = 1
  

def display_rank():
    ranking()
    space = 0
    for i in range(0, 5):
        draw_text_rank(f'{rankscores[i][0]}', ('#61452C'), 50, screen, (screen_width / 2 - 250 + 3, 230 + 3 + space))
        draw_text_rank(f'{rankscores[i][0]}', ('#FFF4EB'), 50, screen, (screen_width / 2 - 250, 230 + space))
        space += 50

    space = 0
    for i in range(0, 5):
        draw_text_rank(f'{rankscores[i][1]}', ('#61452C'), 50, screen, (screen_width / 2 + 200 + 3, 230 + 3 + space))
        draw_text_rank(f'{rankscores[i][1]}', ('#FFF4EB'), 50, screen, (screen_width / 2 + 200, 230 + space))
        space += 50

def draw_text(text, color, size, screen, pos):
    global screen_width, screen_height
    font = pygame.font.Font('../Infographic/font/subatomic.ttf', size)
    textobj = font.render(text, False, color)
    textrect = textobj.get_rect(center=pos)
    screen.blit(textobj, textrect)


def draw_text_rank(text, color, size, screen, pos):
    global screen_width, screen_height
    font = pygame.font.Font('../Infographic/font/subatomic.ttf', size)
    textobj = font.render(text, False, color)
    textrect = textobj.get_rect(midleft=pos)
    screen.blit(textobj, textrect)


def menu():
    while True:
        global screen_width, screen_height, show, prev_player_score, new_player_score
        show = 0
        prev_player_score = 0
        new_player_score = 0
        background_image = pygame.image.load('../Infographic/graphics/other/Background.png')
        screen.blit(background_image, (0, 0))

        draw_text('The Westerner', ('#61452C'), 90, screen,
                  (screen_width/2 + 43, screen_height/2 - 80 + 3))
        draw_text('The Westerner', ('#FFF4EB'), 90, screen,
                  (screen_width/2 + 40, screen_height/2 - 80))

        draw_text('65010107 Khris Bharmmano', ('#61452C'), 30, screen,
                  (screen_width/2 + 43, screen_height/2 + 23))
        draw_text('65010107 Khris Bharmmano', ('#FFF4EB'), 30, screen,
                  (screen_width/2 + 40, screen_height/2 + 20))

        game_button = pygame.Rect((320, 450), (150, 50))
        rank_button = pygame.Rect((610, 450), (150, 50))
        pygame.draw.rect(screen, ('#61452C'), game_button)
        pygame.draw.rect(screen, ('#61452C'), rank_button)

        draw_text('PLAY', ('#FFF4EB'), 50, screen, (400, 473))
        draw_text('RANK', ('#FFF4EB'), 50, screen, (690, 473))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if game_button.collidepoint((mx, my)):
                    game()
                if rank_button.collidepoint((mx, my)):
                    rank()

        pygame.display.update()
        clock.tick(60)


def game():
    while True:
        gamerun.run()


def rank():
    while True:
        background_image = pygame.image.load('../Infographic/graphics/other/Background.png')
        screen.blit(background_image, (0, 0))

        draw_text('RANK', ('#61452C'), 100, screen,
                  (screen_width/2 + 3, 140 + 3))
        draw_text('RANK', ('#FFF4EB'), 100, screen, (screen_width/2, 140))

        menu_button = pygame.Rect((820, 550), (150, 50))
        pygame.draw.rect(screen, ('#61452C'), menu_button)

        draw_text('BACK', ('#FFF4EB'), 50, screen, (900, 580))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if menu_button.collidepoint((mx, my)):
                    menu()

        display_rank()

        pygame.display.update()
        clock.tick(60)

menu()