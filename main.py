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

# Imagens
class Imagem():
    def __init__(self, arquivo ,tamanhox, tamanhoy):
        self.arquivo = arquivo
        self.tamanhox = tamanhox
        self.tamanhoy = tamanhoy
        self.obs = pygame.image.load(self.arquivo).convert_alpha()
        self.obs = pygame.transform.scale(self.obs,(self.tamanhox,self.tamanhoy))

    def carregar(self):
        return self.obs
    
    def plot(self, x, y):
        return screen.blit(self.obs,(x,y))
    
    def retangulo(self):
        return self.obs.get_rect()

imagens = [Imagem('imagens/ladrao.png',100,105), Imagem('imagens/policia.png',100,100), Imagem('imagens/cone.png', 67, 67), Imagem('imagens/pedra.png', 67, 67), Imagem('imagens/roda.PNG', 67, 67), Imagem('imagens/1vida.png',17.5,15), Imagem('imagens/2vidas.png',40,15), Imagem('imagens/3vidas.png',62.5,15)]
for imagem in imagens:
    imagem.carregar()


# Posições iniciais dos Carros
ladrao_x = 200
ladrao_y = 230
policia_x = 300
policia_y = 350

possivel_x = np.arange(110,411,100) # lista de possíveis posições x pro obstáculo
obstaculos = [imagens[2],imagens[3],imagens[4]]

# Texto
font = pygame.font.SysFont(None, 24)
ladraotxt = font.render('LADRÃO', True, (0, 0, 0))
policiatxt = font.render('POLÍCIA', True, (0, 0, 0))


# Numero de batidas de cada carro
batidas_lad = 0
batidas_pol = 0

jogo = True # Variavel para o jogo ficar rodando
obst = False # Variavel 

corquad = (253,196,101) # Cor do Quadrado


# loop do Jogo
while jogo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False

    screen.blit(bg, (0,0))
    velocidade = 1

    # Movimento da Pista
    rel_y = y % bg.get_rect().height
    screen.blit(bg, (0,rel_y - bg.get_rect().height))
    if rel_y < 480:
        screen.blit(bg,(0,rel_y))
    y += velocidade

    # Obstáculos
    if obst == False:
        obs_x = random.choice(possivel_x)
        obs_y = 0
        o = random.choice(obstaculos)
        obst = True
    o.plot(obs_x,obs_y)
    obs_y += velocidade # Movimento  do obstáculo

    if obs_y == 465:
        obst = False # se o obstaculo passar a tela não existem mais obstáculo no jogo

    # Imagens
    imagens[0].plot(ladrao_x,ladrao_y) # Ladrão
    imagens[1].plot(policia_x,policia_y) # Policia


    # Colisões
    ladrao_rect = imagens[0].retangulo()
    policia_rect = imagens[1].retangulo()
    obstaculo_rect = o.retangulo()

    ladrao_rect.x = ladrao_x
    ladrao_rect.y = ladrao_y
    policia_rect.x = policia_x
    policia_rect.y = policia_y
    obstaculo_rect.x = obs_x
    obstaculo_rect.y = obs_y

    pygame.draw.rect(screen, (255,0,0), ladrao_rect, 4)
    pygame.draw.rect(screen, (255,0,0), policia_rect, 4)
    pygame.draw.rect(screen, (255,0,0), obstaculo_rect, 4)

    if ladrao_rect.colliderect(obstaculo_rect):
        batidas_lad += 1
    if policia_rect.colliderect(obstaculo_rect):
        batidas_pol += 1

    # Vidas
    pygame.draw.rect(screen, corquad, pygame.Rect(0,15,87,50)) # Retângulo Vida ladrão
    pygame.draw.rect(screen, corquad, pygame.Rect(513,15,88,50)) # Retângulo Vida Policia
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,15,87,50),4) # Contorno Retângulo Vida ladrão
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(513,15,88,50),4) # Contorno Retângulo Vida Policia

    if batidas_lad == 0:
        imagens[7].plot(15,40)
    elif batidas_lad == 1:
        imagens[6].plot(15,40)
    elif batidas_lad == 2:
        imagens[5].plot(15,40)
    if batidas_pol == 0:
        imagens[7].plot(530,40)
    elif batidas_pol == 1:
        imagens[6].plot(530,40)
    elif batidas_pol == 2:
        imagens[5].plot(530,40)

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