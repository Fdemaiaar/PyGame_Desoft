# Importando Bibliotecas
from importlib.machinery import EXTENSION_SUFFIXES
import pygame
import random
import numpy as np
import os



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

# Musica
arquivo = os.path.join('Imagens', 'background.ogg')
pygame.mixer.music.load(arquivo)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Background
bg = pygame.image.load('imagens/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x,y))

# Imagens Carros
ladrao = pygame.image.load('imagens/ladrao.png').convert_alpha()
ladrao = pygame.transform.scale(ladrao, (100,105)) # Tamanho do ladrao
policia = pygame.image.load('imagens/policia.png').convert_alpha()
policia = pygame.transform.scale(policia, (100,100)) # Tamanho da policia

# Imagens Vidas
vida1 = pygame.image.load('imagens/1vida.png').convert_alpha()
vida1 = pygame.transform.scale(vida1, (17.5,15))
vida2 = pygame.image.load('imagens/2vidas.png').convert_alpha()
vida2 = pygame.transform.scale(vida2, (40,15))
vida3 = pygame.image.load('imagens/3vidas.png').convert_alpha()
vida3 = pygame.transform.scale(vida3, (62.5,15))
corquad = (253,196,101) # Cor do Quadrado

#Obstáculos
class Obstaculo:
    def __init__(self, arquivo ,tamanhox, tamanhoy):
        self.arquivo = arquivo
        self.tamanhox = tamanhox
        self.tamanhoy = tamanhoy
        self.obs = pygame.image.load(self.arquivo).convert_alpha()

    def carregar(self):
        return pygame.transform.scale(self.obs,(self.tamanhox,self.tamanhoy))
    
    def plot(self, x):
        return screen.blit(self.obs,(x,0))

cone = Obstaculo('imagens/cone.png', 10, 10)
pedra = Obstaculo('imagens/pedra.jpg', 10, 10)
roda = Obstaculo('imagens/roda.PNG', 10, 10)
possivel_x = np.arange(110,411,100) # lista de possíveis posições x pro obstáculo
obstaculos = [cone,pedra,roda] # lista para entrar na função


# Texto
font = pygame.font.SysFont(None, 24)
ladraotxt = font.render('LADRÃO', True, (0, 0, 0))
policiatxt = font.render('POLÍCIA', True, (0, 0, 0))


# Numero de batidas de cada carro
batidas_lad = 0
batidas_pol = 0

jogo = True # Variavel para o jogo ficar rodando
obst = False # Variavel 

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
    y += 1

    # Obstáculos
    if obst == False:
        o = random.choice(obstaculos)
        x = random.choice(possivel_x)
        o.carregar()
        obst == True

    o.plot(x)


    # Imagens
    screen.blit(ladrao, (ladrao_x,ladrao_y)) # Ladrão
    screen.blit(policia, (policia_x,policia_y)) # Policia
    pygame.draw.rect(screen, corquad, pygame.Rect(0,15,87,50)) # Retângulo Vida ladrão
    pygame.draw.rect(screen, corquad, pygame.Rect(513,15,88,50)) # Retângulo Vida Policia
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,15,87,50),4) # Contorno Retângulo Vida ladrão
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(513,15,88,50),4) # Contorno Retângulo Vida Policia

    # Colisão


    # Vidas
    if batidas_lad == 0:
        screen.blit(vida3, (15,40))
    if batidas_lad == 1:
        screen.blit(vida2, (15,40))
    if batidas_lad == 2:
        screen.blit(vida1,(15,40))
    if batidas_pol == 0:
        screen.blit(vida3, (530,40))
    if batidas_pol == 1:
        screen.blit(vida2, (530,40))
    if batidas_pol == 2:
        screen.blit(vida1,(530,40))

    # Comandos
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_RIGHT] and policia_x < 400:
        policia_x += 2
    if tecla[pygame.K_LEFT] and policia_x > 102.5:
        policia_x -= 2
    if tecla[pygame.K_d] and ladrao_x < 400:
        ladrao_x += 2
    if tecla[pygame.K_a] and ladrao_x > 102.5:
        ladrao_x -= 2
    
    # Texto das Vidas
    screen.blit(ladraotxt, (9, 20))
    screen.blit(policiatxt, (526, 21))


    pygame.display.update()