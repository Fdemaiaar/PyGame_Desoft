import pygame
import random
import funcoes


pygame.init()  # Iniciando o pygame

x = 600
y = 480

# criando a tela
screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('DustChase')

# Background
bg = pygame.image.load('imagens/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x,y))



jogo = True # Variavel para o jogo ficar rodando

# loop do Jogo
while jogo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False

    screen.blit(bg, (0,0))

    # Movimento da Pista
    rel_y = y % bg.get_rect().height
    screen.blit(bg, (0,rel_y - bg.get_rect().height))
    if rel_y < 480:
        screen.blit(bg,(0,rel_y))
    y += 3 


    pygame.display.update()