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

# Musicas
pygame.mixer.music.set_volume(0.3)
som_sirene = pygame.mixer.music.load('sons/sirene.mp3')
pygame.mixer.music.play(-1)
som_colisao = pygame.mixer.Sound('sons/colisao.wav')
som_colisaof = pygame.mixer.Sound('sons/colisao-final.wav')
som_radio = pygame.mixer.Sound('sons/police-radio.wav')



# Background
bg = pygame.image.load('imagens/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x,y))

# Imagens
class Imagem():
    def __init__(self, arquivo ,tamanhox, tamanhoy):
        self.arquivo = arquivo
        self.tamanhox = tamanhox
        self.tamanhoy = tamanhoy
        self.img = pygame.image.load(self.arquivo).convert_alpha()
        self.img = pygame.transform.scale(self.img,(self.tamanhox,self.tamanhoy))

    def carregar(self):
        return self.img
    
    def plot(self, x, y):
        return screen.blit(self.img,(x,y))
    
    def retangulo(self):
        return (self.img).get_rect()

imagens = {
    'ladrao': Imagem('imagens/ladrao.png',100,105), 
    'policia': Imagem('imagens/policia.png',100,100),
    'cone': Imagem('imagens/cone.png', 67, 67),
    'pedra': Imagem('imagens/pedra.png', 67, 67),
    'roda': Imagem('imagens/roda.PNG', 67, 67),
    '1vida': Imagem('imagens/1vida.png',17.5,15),
    '2vidas': Imagem('imagens/2vidas.png',40,15),
    '3vidas': Imagem('imagens/3vidas.png',62.5,15),
    'entrada': Imagem('imagens/foto-entrada.png', 380,320),
    'vitlad':Imagem('imagens/vitlad.png', 490,370),
    'vitpol':Imagem('imagens/vitpol.png', 490,370)
}

for imagem in imagens.values():
    imagem.carregar()

# Posições iniciais dos Carros
ladrao_x = 200
ladrao_y = 230
policia_x = 300
policia_y = 350

possivel_x = np.arange(110,411,100) # lista de possíveis posições x pro obstáculo
obstaculos = [imagens['cone'],imagens['pedra'],imagens['roda']]

# Texto
font = pygame.font.SysFont(None, 24)
ladraotxt = font.render('LADRÃO', True, (0, 0, 0))
policiatxt = font.render('POLÍCIA', True, (0, 0, 0))


# Numero de batidas de cada carro
batidas_lad = 0
batidas_pol = 0
velocidade = 0

jogo = True # Variavel para o jogo ficar rodando
obst = False # Variavel para os obstáculos
entrada = True # Variavel para a musica da entrada
radio = False # Variavel para o radio policial
reentrada_p = False
reentrada_l = False

corquad = (253,196,101) # Cor do Quadrado

def colisao():
    global batidas_lad
    global batidas_pol
    global velocidade
    if ladrao_rect.colliderect(obstaculo_rect):
        batidas_lad += 1
        if batidas_lad == 3:
            velocidade = 0
            som_colisaof.play()
        else:
            som_colisao.play()
        return True
    if policia_rect.colliderect(obstaculo_rect):
        batidas_pol += 1
        if batidas_pol == 3:
            velocidade = 0 
            som_colisaof.play()
        else:
            som_colisao.play()           
        return True
    else:
        return False
        

# loop do Jogo
while jogo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo = False # Encerra o jogo quando o usuário sai da tela

    screen.blit(bg, (0,0))
    tecla = pygame.key.get_pressed()

    # Entrada Do Jogo
    if entrada:
        imagens['entrada'].plot(110,70)
    if reentrada_p:
        imagens['vitpol'].plot(44,40)
    if reentrada_l:
        imagens['vitlad'].plot(90,65)
    if tecla[pygame.K_SPACE]:
        som_radio.play()
        velocidade = 2
        entrada = False
        reentrada_p = False
        reentrada_l = False

    if velocidade > 0:

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


        # Imagens
        imagens['ladrao'].plot(ladrao_x,ladrao_y) # Ladrão
        imagens['policia'].plot(policia_x,policia_y) # Policia


        # Colisões
        ladrao_rect = pygame.Rect((ladrao_x + 24),ladrao_y,52,100)
        policia_rect = pygame.Rect((policia_x + 23),policia_y,52,100)
        obstaculo_rect = o.retangulo()

        obstaculo_rect.x = obs_x
        obstaculo_rect.y = obs_y

        if colisao() or obs_y == 465: # se o obstaculo passar a tela ou tiver uma colisao
            obst = False

        # Vidas
        pygame.draw.rect(screen, corquad, pygame.Rect(0,15,87,50)) # Retângulo Vida ladrão
        pygame.draw.rect(screen, corquad, pygame.Rect(513,15,88,50)) # Retângulo Vida Policia
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,15,87,50),4) # Contorno Retângulo Vida ladrão
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(513,15,88,50),4) # Contorno Retângulo Vida Policia

        if batidas_lad == 0:
            imagens['3vidas'].plot(15,40)
        if batidas_lad == 1:
            imagens['2vidas'].plot(15,40)
        if batidas_lad == 2:
            imagens['1vida'].plot(15,40)
        if batidas_pol == 0:
            imagens['3vidas'].plot(530,40)
        if batidas_pol == 1:
            imagens['2vidas'].plot(530,40)
        if batidas_pol == 2:
            imagens['1vida'].plot(530,40)

        # Comandos
        if velocidade != 0:
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

    # Renovando as Vidas e declarando vitória
    if batidas_lad == 3:
        batidas_lad = 0
        batidas_pol = 0
        reentrada_p = True
    if batidas_pol == 3:
        batidas_lad = 0
        batidas_pol = 0
        reentrada_l = True
        

    pygame.display.update()