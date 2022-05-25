import pygame
import random
import funcoes


pygame.init()  # Iniciando o pygame

# Tamanho da tela
x = 600
y = 480

# Posições iniciais dos Carros
ladrao_x = 200
ladrao_y = 230
policia_x = 300
policia_y = 350

# criando a tela
screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('DustChase')

# Background
bg = pygame.image.load('imagens/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x,y))

# Carros
ladrao = pygame.image.load('imagens/ladrao.png').convert_alpha()
ladrao = pygame.transform.scale(ladrao, (100,105)) # Tamanho do ladrao
policia = pygame.image.load('imagens/policia.png').convert_alpha()
policia = pygame.transform.scale(policia, (100,100)) # Tamanho da policia

# Vidas
vida1 = pygame.image.load('imagens/1vida.png').convert_alpha()
vida1 = pygame.transform.scale(vida1, (14,12))
vida2 = pygame.image.load('imagens/2vidas.png').convert_alpha()
vida2 = pygame.transform.scale(vida2, (32,12))
vida3 = pygame.image.load('imagens/3vidas.png').convert_alpha()
vida3 = pygame.transform.scale(vida3, (50,12))



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
    y += 0.80

    screen.blit(ladrao, (ladrao_x,ladrao_y))
    screen.blit(policia, (policia_x,policia_y))
    screen.blit(vida3, (20,20))


    pygame.display.update()