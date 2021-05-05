#Space Learners
#Rafael Cardenuto
#Juliano Gomes

import sys
import math
import pygame
import random
import getpass
import time
from pygame.locals import *
from sys import exit
from bancopalavras import bancodeFases
from geometria import *
from tratarArquivo import *

pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()
SCREEN_SIZE =(800,600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0 ,32)
RAIO_SPRITES = 50
FPS = 60
username = getpass.getuser()

#Sons
musica = True
efeitos_sonoros = True

#Fontes

spaceAdventure = "fonts/SpaceAdventure.ttf"
spaceFont2 = "fonts/SpaceFont2.ttf"
arial = "arial"
tahoma = "Tahoma"

#Sprites Utilizados

#Obstaculos
explosion_sprite = 'sprites/explosion.png'
borracha = 'sprites/borracha.png'
lapis = 'sprites/lapis.png'
tesoura = 'sprites/tesoura.png'
cola = 'sprites/cola.png'
caderno = 'sprites/caderno.png'
bomb = 'sprites/bomba.png'

#Somente para Menu Principal
borracha_bw = 'sprites/borracha-bw.png'
lapis_bw = 'sprites/lapis-bw.png'
tesoura_bw = 'sprites/tesoura-bw.png'
cola_bw = 'sprites/cola-bw.png'
caderno_bw = 'sprites/caderno-bw.png'

#PowerUps
ampulheta = 'sprites/ampulheta.png'
ampulheta_p ='sprites/ampulheta2.png'
one_up = 'sprites/1up.png'
nuke = 'sprites/nuke.png'
nuke_p ='sprites/nuke2.png'

#Sons
music_on = 'sprites/music on.png'
music_off = 'sprites/music off.png'
effects_on = 'sprites/effects_on.png'
effects_off = 'sprites/effects_off.png'

#Jogador
kevin_sprite = 'sprites/kevin.png'
bullet_sprite = 'sprites/bullet.png'
vida= 'sprites/life.png'

next_level_sprite = 'sprites/next_level.png'

#Kromb
kromb_sprite1 = 'sprites/alien_2.png'
kromb_sprite2 = 'sprites/alien_1.png'
kromb_sprite_shield = 'sprites/alien_shield.png'
kromb_sprite_damaged = 'sprites/alien_damaged.png'

#Nave
nave_vermelha = 'sprites/nave-vermelha.png'
nave_rosa = 'sprites/nave-rosa.png'
nave_verde ='sprites/nave-verde.png'
nave_azul_escura = 'sprites/nave-azul-escura.png'
nave_amarela = 'sprites/nave-amarela.png'
nave_azul =  'sprites/nave-azul.png'
nave_preta = 'sprites/nave-preta.png'
nave_laranja =  'sprites/nave-laranja.png'
nave_verde_escura = 'sprites/nave-verde-escura.png'
nave_spawn = 'sprites/nave-spawn.png'

def create_retangulo(x,y,w,h):
    rect = pygame.Rect(x,y,w,h)

    return rect
def cria_palavras(palavras):
    vetor = []
    for x in range(0,3,1):
        txt = Palavra(palavras[x])
        vetor.append(txt)
    return vetor

#Classe Nave Jogador
class Nave(object):
    def __init__(self,sprite,x,y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.pontos = 0
        self.vidas = 3
        self.raio = 33
        self.circulo = Circulo(x,y,33)
        self.powerup = 'none'
        self.estado = 'jogando'
        self.tempospawn = 0

    def move(self,increm_x,increm_y):
        self.x +=increm_x
        self.y +=increm_y
        self.circulo.x = self.x
        self.circulo.y = self.y
        if self.x + 50 >= 800:
            self.x = 750
        if self.x - 40 < 0:
            self.x = 50
        if self.y + 30 >= 600:
            self.y = 570
        if self.y -50 < 0:
            self.y = 50

    def resetPosicaoInicial(self):
        self.x = 400
        self.y = 550

    def ganhaVida(self):
        self.vidas += 1
        if self.vidas==4:
            self.vidas = 3
        if(efeitos_sonoros == True): 
            pygame.mixer.Channel(1).set_volume(0.02)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Audio/extra-life.wav'))

    def perdeVida(self):
        self.vidas -= 1

    def update(self):
        if self.pontos<0:
            self.pontos = 0

class Fase(object):
    def __init__(self,palavras,frase,vel):
        self.ordem = cria_palavras(palavras)
        self.completa = False
        self.nivel = vel
        self.ordemJogador = []
        self.frase = frase
        self.estado = 'rolando'
        self.tempo = 200
        self.pontospravida = 5000
        self.contador = 0
        self.existePowerUp = False
        self.powerup = ''
        self.faseBoss = False


    def resetFase(self):
        self.ordemJogador = []
        self.estado = 'rolando'
        for i in self.ordem:
                i.colidiu = False
                i.redirecionar()

    def update(self):
        for i in self.ordem:
            if not i.colidiu:
                i.move()

        for i in range(0,3,1):
            for j in range(0,3,1):
                if j!=i:
                    if intersectRR(self.ordem[i].retangulo,self.ordem[j].retangulo):
                        self.ordem[i].redirecionar()
                        self.ordem[j].redirecionar()
        if self.faseBoss == False:
            if self.tempo <= 0:
                self.estado = 'perdida'


    def testarOrdem(self):
        if self.estado == 'rolando':
            if len(self.ordemJogador)==3:
                if self.ordem[0].texto==self.ordemJogador[0] and self.ordem[1].texto==self.ordemJogador[1] and self.ordem[2].texto==self.ordemJogador[2]:
                    self.estado = 'acertou'
                else:
                    self.estado='errou'
    def draw(self,win):
        font = pygame.font.SysFont(tahoma, 16,bold=True)  # Fonte para escrever na tela
        fontTempo = pygame.font.Font(spaceAdventure, 16)  # Fonte para tempo de partida
        if self.faseBoss:
            if self.estado == 'rolando':
                for i in self.ordem:
                    if not i.colidiu:
                        i.draw(win,self.faseBoss)

                cor = (0, 255, 0)
                text = font.render(self.frase, False, cor, (0, 0, 0))
                win.blit(text, (int(SCREEN_SIZE[0] / 2 - text.get_width() / 2), 20))

            elif self.estado == 'acertou':
                msg = 'Você acertou!!! Agora use a nuke!!'
                text = font.render(msg, False, (0, 255, 0), (0, 0, 0))
                win.blit(text, (int(SCREEN_SIZE[0] / 2 - text.get_width() / 2), 10))
            elif self.estado == 'errou' or self.estado == 'reiniciando':
                msg = 'Ordem errada!'
                text = font.render(msg, False, (255, 0, 0), (0, 0, 0))
                win.blit(text, (int(SCREEN_SIZE[0] / 2 - text.get_width() / 2), 25))
        else:
            if self.estado == 'rolando':
                msg = 'Tempo : ' + str(self.tempo)
                text = fontTempo.render(msg, False, (0, 255, 0))
                win.blit(text, (20, 10))
                for i in self.ordem:
                    if not i.colidiu:
                        i.draw(win,self.faseBoss)

                cor = (0, 255, 0)
                text = font.render(self.frase, False, cor, (0, 0, 0))
                win.blit(text, (int(SCREEN_SIZE[0]/2 - text.get_width()/2), 10))
                if self.contador==2:
                    msg = 'Falta uma frase!! '
                    text = font.render(msg, False, cor, (0, 0, 0))
                    win.blit(text, (int(SCREEN_SIZE[0] / 2 - text.get_width() / 2), 35))
                elif self.contador==1:
                    msg = 'Precisa acertar mais duas!! '
                    text = font.render(msg, False, cor, (0, 0, 0))
                    win.blit(text, (int(SCREEN_SIZE[0] / 2 - text.get_width() / 2), 35))

            elif self.estado == 'acertou':
                msg = 'Você acertou as três frases!!! Agora escape desta fase!!'
                text = font.render(msg, False, (0,255,0),(0,0,0))
                win.blit(text, (int(SCREEN_SIZE[0] / 2 - text.get_width() / 2), 10))
            elif self.estado == 'errou' or self.estado=='reiniciando':
                msg = 'Ordem errada!'
                text = font.render(msg,False,(255,0,0),(0,0,0))
                win.blit(text, (int(SCREEN_SIZE[0]/2 - text.get_width()/2), 25))

class Palavra(object):
    def __init__(self, texto):
        self.texto = texto.upper()
        self.x = random.randint(0,SCREEN_SIZE[0])+10
        self.y = random.randint(0,SCREEN_SIZE[1]/2)+10
        self.retangulo = Retangulo(self.x,self.y,10,10)
        self.colidiu = False
        self.dx = random.randint(0,SCREEN_SIZE[0])
        self.dy = random.randint(0,SCREEN_SIZE[1])


    def draw(self,win,boss):
        if boss:
            cor = (255,165,0)
        else:
            cor = (0,0,0)
        font = pygame.font.SysFont(tahoma, 22,bold=True)
        text = font.render(self.texto,False, cor)
        self.retangulo.w = int(text.get_width())
        self.retangulo.h = int(text.get_height())
        #pygame.draw.rect(win, (0, 0, 0), (self.retangulo.x, self.retangulo.y, self.retangulo.w, self.retangulo.h))
        win.blit(text, (self.x ,self.y ))


    def redirecionar(self):
        tempo = random.randint(0,10)
        if tempo<3:
            self.x = random.randint(0, 800)
            self.y = 0
        elif tempo<5:
            self.x = 0
            self.y = random.randint(0, 400)
        elif tempo<8:
            self.x = 100
            self.y = random.randint(0, 400)
        elif tempo<=10:
            self.x = random.randint(0, 800)
            self.y = 0


    def move(self):
        self.retangulo.x = self.x
        self.retangulo.y = self.y
        if (self.x <= 0 or self.x + self.retangulo.w >= 700 or self.y <= 50 or self.y >= 500) or (self.dx == self.x and self.dy == self.y):
            self.dx = random.randint(0, 800)
            self.dy = random.randint(0, 600)
        if self.dx-self.x > 0:
            self.x += 1
        elif self.dx-self.x < 0:
            self.x -= 1
        if self.dy - self.y > 0:
            self.y += 1
        elif self.dy - self.y < 0:
            self.y -= 1

    def colisaoNavePalavra(self,ast1):
        if intersectRC(self.retangulo,ast1.circulo):
            return True
        return False

class Portal(object):
    def __init__(self,sprite):
        self.sprite = sprite
        self.x = int(SCREEN_SIZE[0]/2)
        self.y = int(SCREEN_SIZE[1]/2)
        self.colidiu = False
        self.raio = 30

    def draw(self,win):
        win.blit(self.sprite,(int(self.x - self.sprite.get_width()/2),int(self.y - self.sprite.get_height()/2)))


    def colisao(self,ast1):
        distancia = math.sqrt(((ast1.x - self.x) ** 2) + ((ast1.y - self.y) ** 2))
        if (ast1.raio + self.raio) >= distancia:
            return True
        return False
#Classe dos Tiros
class Bullet(object):
    def __init__(self,sprite,x,y):
        self.sprite = sprite
        self.x = x +20
        self.y = y+20
        self.colisao = False
        self.retangulo = Retangulo(self.x,self.y,20,35)

    def move(self):
        self.y -=30
        self.retangulo.x = self.x -10
        self.retangulo.y = self.y-20


#Classe para obstaculos - modificar para criar sprites em vez de circulos
class Asteroide(object):
    def __init__(self,op,vel):
        self.vel_inicial = vel #controle de velocidade
        self.vel = vel
        if (op == 0):
            obst_image_filename = borracha
            self.x = random.randint(0,SCREEN_SIZE[0]-100)
            self.y = -50 
            self.raio = 25
            self.increm_x = 0
            self.increm_y = self.vel
        elif (op == 1):
            obst_image_filename = lapis
            self.x = random.randint(0, SCREEN_SIZE[0]-100)
            self.y = 0 
            self.raio = 15
            self.increm_x = 0
            self.increm_y = self.vel 
        elif (op == 2):
            obst_image_filename = tesoura
            self.x = -50 
            self.y = random.randint(0, SCREEN_SIZE[1]-50)
            self.raio = 35
            self.increm_x = self.vel 
            self.increm_y = 0
        elif (op == 3):
            obst_image_filename = cola
            self.x = SCREEN_SIZE[1]+100
            self.y = random.randint(0, SCREEN_SIZE[1]-50)
            self.raio = 33
            self.increm_x = -self.vel 
            self.increm_y = 0
        elif (op == 4):
            obst_image_filename = caderno
            self.x = random.randint(0, SCREEN_SIZE[0]-100)
            self.y = 50
            self.raio = 40
            self.increm_x = 0
            self.increm_y = self.vel 
        elif(op == 5):
            obst_image_filename = bomb
            self.x = 50 
            self.y = 50 
            self.raio = 15
            self.increm_x = 0
            self.increm_y = self.vel 
        if (op == 6):
            obst_image_filename = borracha_bw
            self.x = random.randint(0,SCREEN_SIZE[0]-50)
            self.y = 50 
            self.raio = 25
            self.increm_x = 0
            self.increm_y = self.vel
        elif (op == 7):
            obst_image_filename = lapis_bw
            self.x = random.randint(0, SCREEN_SIZE[0]-50)
            self.y = 50 
            self.raio = 15
            self.increm_x = 0
            self.increm_y = self.vel 
        elif (op == 8):
            obst_image_filename = tesoura_bw
            self.x = 50 
            self.y = random.randint(0, SCREEN_SIZE[1]-50)
            self.raio = 35
            self.increm_x = self.vel 
            self.increm_y = 0
        elif (op == 9):
            obst_image_filename = cola_bw
            self.x = SCREEN_SIZE[1]+50
            self.y = random.randint(0, SCREEN_SIZE[1]-50)
            self.raio = 33
            self.increm_x = -self.vel 
            self.increm_y = 0
        elif(op == 10):
            obst_image_filename = caderno_bw
            self.x = random.randint(0, SCREEN_SIZE[0]-50)
            self.y = 50 
            self.raio = 40
            self.increm_x = 0
            self.increm_y = self.vel 
        
            
        self.x += 50
        self.y += 50
        self.colisao = False
        self.circulo = Circulo(self.x,self.y,self.raio)
        self.ativo = False
        self.sprite = pygame.image.load(obst_image_filename).convert_alpha()
        self.op = op

    def update(self):
        if (self.op == 0):
            self.increm_y = self.vel
        elif (self.op == 1):
            self.increm_y = self.vel
        elif (self.op == 2):
            self.increm_x = self.vel
        elif (self.op == 3):
            self.increm_x = -self.vel
        else:
            self.increm_y = self.vel

    def move(self):
        self.x += self.increm_x
        self.y += self.increm_y
        self.circulo.x = self.x
        self.circulo.y = self.y
        # Impedir de sair da tela
        if self.ativo:
            if self.x >= 800 or self.x <= 0:
                self.increm_x *= -1
            if self.y >= 600 or self.y <= 0:
                self.increm_y *= -1
        else:
            if self.x < 800 and self.x > 0:
                self.ativo = True
            if self.y < 600 and self.y > 0:
                self.ativo = True
                
class Vida(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Botao(object):
    def __init__(self,rect, dimensoes,cor,tipo,text,text_rect,center):
        self.rect = rect
        self.dimensoes = dimensoes
        self.cor = cor
        self.tipo = tipo
        self.text = text
        self.text_rect = text_rect
        self.text_rect.center = center

class Button:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.musica = True
        self.tipo = tipo
        if tipo=='som':
            self.sprite = pygame.image.load(effects_on).convert_alpha()
        elif tipo=='musica':
            self.sprite =  pygame.image.load(music_on).convert_alpha()

    def update(self):
        if self.musica:
            self.musica = False
        else:
            self.musica = True

        if self.musica:
            if self.tipo == 'som':
                self.sprite = pygame.image.load(effects_on).convert_alpha()
            elif self.tipo == 'musica':
                self.sprite = pygame.image.load(music_on).convert_alpha()
        else:
            if self.tipo == 'som':
                self.sprite = pygame.image.load(effects_off).convert_alpha()
            elif self.tipo == 'musica':
                self.sprite = pygame.image.load(music_off).convert_alpha()

    def draw(self, win):
        pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, (0,255,0), (self.x, self.y, self.width, self.height),1)
        win.blit(self.sprite,(self.x+5, self.y+5, self.width, self.height))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
class Kromb(object):
    def __init__(self,sprite,x,y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.vx = 10
        self.vy = 0
        self.vida = 300
        self.raio = 80
        self.circulo = Circulo(x,y,88)
        self.estado = 'atacando'
        self.estadovida = 'cheia'
        self.frameDano = 0

    def move(self):
        delta_t = 0.05
        m=1
        k = 0.5 #Spring Constant
         
        fx = 0
        fy = -k * (self.y-150)
        self.vx = self.vx + (fx / m) * delta_t #precisa ser negativa pra trocar
        self.vy = self.vy + (fy / m) * delta_t
        self.x = self.x + self.vx * delta_t #precisa ser negativa pra trocar
        self.y = self.y + self.vy * delta_t
        self.circulo.x = self.x
        self.circulo.y = self.y
        if self.x+75>=800 or self.x-75<=0:
            self.vx *= -1
        #depois colocar movimento de mola

    def perdeVida(self):
        self.vida -= 1

    
def colisao(ast1, ast2):
    distancia =  math.sqrt(((ast1.x-ast2.x)**2)+((ast1.y-ast2.y)**2))
    if (ast1.raio + ast2.raio) >= distancia:
        ast1.sprite = pygame.image.load(explosion_sprite).convert_alpha()
        ast2.sprite = pygame.image.load(explosion_sprite).convert_alpha()
        ast1.colisao = True
        ast2.colisao = True
        if(efeitos_sonoros == True):
            pygame.mixer.Channel(0).set_volume(0.008)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Audio/explosion2.wav'), maxtime=600)
        
        return True
    else:
        return False

def colisaoBala(ast1, ast2):
    if intersectRC(ast1.retangulo,ast2.circulo):
        ast1.sprite = pygame.image.load(explosion_sprite).convert_alpha()
        ast2.sprite = pygame.image.load(explosion_sprite).convert_alpha()
        ast1.colisao = True
        ast2.colisao = True
        if(efeitos_sonoros == True):
            pygame.mixer.Channel(0).set_volume(0.008)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Audio/explosion2.wav'), maxtime=600)
        return True
    else:
        return False

def colisaoNaveAsteroide(ast1, ast2):
    #Distancia euclidiana de 2 pontos (centros circunferencias)
    distancia =  math.sqrt(((ast1.x-ast2.x)**2)+((ast1.y-ast2.y)**2))
    if (ast1.raio + ast2.raio) >= distancia:
        if ast1.estado == 'nascendo':
            return False
        else:
            ast2.sprite = pygame.image.load(explosion_sprite).convert_alpha()
            ast2.colisao = True
            ast1.resetPosicaoInicial()
            if(efeitos_sonoros == True):
                pygame.mixer.Channel(0).set_volume(0.008)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('Audio/explosion2.wav'), maxtime=600)
            return True
    else:
        return False
    
def blit_text(surface, text, pos, font, color=pygame.Color('green')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
        
class PowerUp(object):
    def __init__(self, i):
        self.x = random.randint(0,SCREEN_SIZE[0])+10
        self.y = random.randint(0,SCREEN_SIZE[1]/2)+10
        self.colidiu = False
        self.dx = random.randint(0,SCREEN_SIZE[0])
        self.dy = random.randint(0,SCREEN_SIZE[1])
        if i==0:
            powerup_image = 'sprites/ampulheta.png'
            self.retangulo = Retangulo(self.x-20, self.y-22, 38, 46)
            self.tipo = 'ampulheta'
        elif i==1:
            powerup_image = 'sprites/1up.png'
            self.circulo = Circulo(self.x, self.y, 40)
            self.tipo = '1up'
        else:
            powerup_image = 'sprites/nuke.png'
            self.retangulo = Retangulo(self.x-20, self.y-35, 40, 70)
            self.tipo = 'nuke'
        self.sprite = pygame.image.load(powerup_image).convert_alpha()

    def draw(self,win):
        win.blit(self.sprite, (int(self.x - self.sprite.get_width() / 2), int(self.y - self.sprite.get_height() / 2)))
        #if self.tipo == '1up':
         #   pygame.draw.circle(win, (255, 0, 0), (self.circulo.x, self.circulo.y), self.circulo.r, 1)
        #else:
         #   pygame.draw.rect(win,(0,0,0),(self.retangulo.x,self.retangulo.y,self.retangulo.w,self.retangulo.h),2)


    def move(self):
        if self.tipo=='ampulheta':
            self.retangulo.x = self.x-20
            self.retangulo.y = self.y-22
        elif self.tipo == 'nuke':
            self.retangulo.x = self.x - 20
            self.retangulo.y = self.y - 35
        else:
            self.circulo.x = self.x
            self.circulo.y = self.y
        if (self.x <= 0 or self.x  >= 700 or self.y <= 50 or self.y >= 500) or (self.dx == self.x and self.dy == self.y):
            self.dx = random.randint(0, 800)
            self.dy = random.randint(0, 600)
        if self.dx-self.x > 0:
            self.x += 1
        elif self.dx-self.x < 0:
            self.x -= 1
        if self.dy - self.y > 0:
            self.y += 1
        elif self.dy - self.y < 0:
            self.y -= 1

    def colisaoComNave(self,ast1):
        if self.tipo=='1up':
            distancia = math.sqrt(((ast1.x - self.circulo.x) ** 2) + ((ast1.y - self.circulo.y) ** 2))
            if (ast1.raio + self.circulo.r) >= distancia:
                return True
            return False
        else:
            if intersectRC(self.retangulo,ast1.circulo):
                return True
            return False

def desenharPowerUp(powerup):
    if (powerup != "none"):
        if (powerup == "nuke"):
            powerup = pygame.image.load(nuke_p).convert_alpha()

        else:
            powerup = pygame.image.load(ampulheta_p).convert_alpha()

        screen.blit(powerup, (15, 525, 40, 60))
    else:
        pygame.draw.rect(screen, (0, 0, 0), (15, 525, 40, 60))


def powerup_release(powerup, obstaculos):
    if (powerup == "nuke"):
        nuke(obstaculos)
        limite_powerup = FPS * 4
    else:
        ampulheta(obstaculos)
        limite_powerup = FPS * 5 #Reduzido um pouco


    return limite_powerup

def nuke(lista):
    for i in range(0,len(lista),1):
        lista[i].sprite = pygame.image.load(explosion_sprite).convert_alpha()
        lista[i].colisao = True
        if(efeitos_sonoros == True): 
            pygame.mixer.Channel(1).set_volume(0.02)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Audio/nuke.wav'))

def ampulheta(lista):
    for i in range(0,len(lista),1):
        lista[i].vel = 0
        lista[i].update()

def normalizaVelocidade(lista):
    for i in range(0,len(lista),1):
        lista[i].vel = lista[i].vel_inicial #Desconsidera velocidade em demais niveis
        lista[i].update()

def testePowerup():
    t = pygame.time.get_ticks()
    if t%55==0:
        return True
    return False

def colisaoBotoes(botoes,held):
    sair = 0
    #Percorre todos os botoes verificando se mouse clicou ou passou sobre eles
    for i in range(0,len(botoes),1):
        if(botoes[i].rect.collidepoint(pygame.mouse.get_pos()) and held):
            botoes[i] = (255,255,255)
            if(botoes.tipo == "sair"):
                sair = -1
            elif(botoes.tipo == "jogar"):
                 sair = 1
            elif(botoes.tipo == "instruc"):
                sair = 2
            elif(botoes.tipo == "proximo"):
                sair = 3
            elif(botoes.tipo == "pularHistoria"):
                sair = 4
            elif(botoes.tipo == "musica"):
                if(musica == False):
                    musica=True
                else:
                    musica=False
            elif(botoes.tipo == "efeitos"):
                if(efeitos_sonoros == False):
                    efeitos_sonoros=True
                else:
                    efeitos_sonoros=False
        elif(botoes[i].rect.collidepoint(pygame.mouse.get_pos())):
              botoes[i] = (255,255,255)
        else:
             botoes[i] = (0,0,0)
                    
    return sair


def pularHistoria():
    sair = 0
    held = False
    w, h = 50, 50
    x, y = 0, 0

    # Background
    background_image_filename = 'Images/background/pularHistoria.png'
    background = pygame.image.load(background_image_filename).convert_alpha()

    # Textos

    pergunta_text = 'Deseja assistir a introdução?'
    pergunta_font = pygame.font.SysFont(tahoma, 25, bold=True) # Fonte para escrever na tela
    
    btn_font = pygame.font.SysFont(tahoma, 16, bold=True) # Fonte para escrever na tela

    btn_assistir_text = btn_font.render('Assistir', True, (0, 255, 0))

    btn_pular_text = btn_font.render('Pular', True, (0, 255, 0))

    btn_voltar_menu_text = btn_font.render('Voltar ao Menu', True, (0, 255, 0))

    # Retangulos dos Textos

    btn_assistir_Rect = btn_assistir_text.get_rect()
    btn_assistir_Rect.center = (420, 145)
    botao_assistir_cor = (0, 0, 0)

    btn_pular_Rect = btn_pular_text.get_rect()
    btn_pular_Rect.center = (420, 235)
    botao_pular_cor = (0, 0, 0)

    btn_voltar_menu_Rect = btn_voltar_menu_text.get_rect()
    btn_voltar_menu_Rect.center = (420, 325)
    botao_voltar_menu_cor = (0, 0, 0)

    while (sair == 0):
        x_draw, y_draw = 100, 70
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x, y = pygame.mouse.get_pos()
                # Para ajustar o movimento (centralizar mouse com retangulo)
                x -= w / 2
                y -= h / 2
            # Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held = True
            if event.type == MOUSEBUTTONUP:
                held = False

        screen.fill((255, 255, 255))

        # Background
        screen.blit(background, (0, 0))

        # Desenhar Pergunta

        #screen.blit(pergunta_text, pergunta_Rect)
        blit_text(screen, 'Deseja assistir a introdução?', (240, 75), pergunta_font)


        # Botoes
        botao_assistir_rect = create_retangulo(320, 130, 200, 30)
        pygame.draw.rect(screen, (0, 255, 0), botao_assistir_rect, 3)
        pygame.draw.rect(screen, botao_assistir_cor, (320, 130, 200, 30))
        screen.blit(btn_assistir_text, btn_assistir_Rect)

        botao_pular_rect = create_retangulo(320, 220, 200, 30)
        pygame.draw.rect(screen, (0, 255, 0), botao_pular_rect, 3)
        pygame.draw.rect(screen, botao_pular_cor, (320, 220, 200, 30))
        screen.blit(btn_pular_text, btn_pular_Rect)

        botao_voltar_menu_rect = create_retangulo(320, 310, 200, 30)
        pygame.draw.rect(screen, (0, 255, 0), botao_voltar_menu_rect, 3)
        pygame.draw.rect(screen, botao_voltar_menu_cor, (320, 310, 200, 30))
        screen.blit(btn_voltar_menu_text, btn_voltar_menu_Rect)

        # Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:
        if (botao_assistir_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_assistir_cor = (255, 255, 255)
            sair = 1
        elif (botao_assistir_rect.collidepoint(pygame.mouse.get_pos())):
            botao_assistir_cor = (255, 255, 255)
        else:
            botao_assistir_cor = (0, 0, 0)

        if (botao_pular_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_pular_cor = (255, 255, 255)
            sair = -1
        elif (botao_pular_rect.collidepoint(pygame.mouse.get_pos())):
            botao_pular_cor = (255, 255, 255)
        else:
            botao_pular_cor = (0, 0, 0)

        if (botao_voltar_menu_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_voltar_menu_cor = (255, 255, 255)
            sair = -2
        elif (botao_voltar_menu_rect.collidepoint(pygame.mouse.get_pos())):
            botao_voltar_menu_cor = (255, 255, 255)
        else:
            botao_voltar_menu_cor = (0, 0, 0)

        pygame.display.update()
    return sair

def rodarHistoria(imagens, dialogos):
    sair = False
    held = False
    w, h = 50, 50
    x, y = 0, 0
    i = 0
    # cenarios teste

    btn_font = pygame.font.SysFont('tahoma', 17,bold=True)  # Fonte para escrever na tela

    btn_text = btn_font.render('Próximo', True, (0, 255, 0))
    dialogo_text = btn_font.render(dialogos[0], True, (0, 255, 0))
    btn_sair = btn_font.render('Pular', True, (0, 255, 0))

    btnRect = btn_text.get_rect()
    btnRect.center = (730, 365)
    btnSair = btn_text.get_rect()
    btnSair.center = (610, 365)
    botao_cor = (0, 0, 0)
    botaosair_cor = (0,0,0)

    dialogoRect = btn_text.get_rect()
    dialogoRect.center = (100, 450)

    while (sair == False):
        background_image_filename = imagens[i]
        dialogo_text = btn_font.render(dialogos[i], True, (0, 255, 0))
        background = pygame.image.load(background_image_filename).convert_alpha()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x, y = pygame.mouse.get_pos()
                x -= w / 2
                y -= h / 2
            # Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held = True
            if event.type == MOUSEBUTTONUP:
                held = False

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 800, 400))
        screen.blit(background, (0, 0))  # cenario
        pygame.draw.rect(screen, (0, 0, 50), (0, 401, 800, 200))
        pygame.draw.rect(screen, (0, 255, 0), (0, 400, 800, 200), 3)

        botao_rect = create_retangulo(680, 340, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), botao_rect, 3)
        pygame.draw.rect(screen, botao_cor, (680, 340, 100, 50))
        screen.blit(btn_text, btnRect)

        botaosair_rect = create_retangulo(550, 340, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), botaosair_rect, 3)
        pygame.draw.rect(screen, botaosair_cor, (550, 340, 100, 50))
        screen.blit(btn_sair, btnSair)

        # screen.blit(dialogo_text, dialogoRect)
        blit_text(screen, dialogos[i], (20, 410), btn_font)

        if (botao_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_cor = (255, 255, 255)
            i += 1
            if (i == len(imagens)):
                sair = True
            time.sleep(0.3)
        elif (botao_rect.collidepoint(pygame.mouse.get_pos())):
            botao_cor = (255, 255, 255)
        else:
            botao_cor = (0, 0, 0)

        if (botaosair_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botaosair_cor = (255, 255, 255)
            sair = True
            time.sleep(0.3)
        elif (botaosair_rect.collidepoint(pygame.mouse.get_pos())):
            botaosair_cor = (255, 255, 255)
        else:
            botaosair_cor = (0, 0, 0)

        pygame.display.update()
        
        
def historia(tipo):
 
    if(tipo == "intro"):

        imagens = ['Images/cenarios/cenario1.png', 'Images/cenarios/cenario2.png', 'Images/cenarios/cenario3.png',
                   'Images/cenarios/cenario4.png', 'Images/cenarios/cenario5(edit).png', 'Images/cenarios/cenario5(edit).png',
                   'Images/cenarios/cenario6.png']

        dialogos = ['Em um dia comum de serviço, podemos ver o piloto Kevin K em seu habitat natural. \n\n' +
                    'O piloto da aliança intergaláctica agora dono da nave mais resistente da Galáxia (adequadamente nomeada de USS Galactica), ' +
                    'estava relaxando tomando um pouco de sol quando de repente...',

                    'Um ataque surpresa se inicia! \n\nKevin: Malditos Krombs!' +
                    ' Esses aliens trabalham até durante fins de semana!?\n\nConstantemente os Krombs atiram bombas na USS Galactica danificando seus escudos',

                    'Kevin tenta saltar para o hiperespaço com sua nave para escapar dos Krombs, mas as bombas que colidiram com a nave afetaram ' +
                    'o componente que permite tal salto.\n\nOcorre então uma explosão e Kevin e sua nave são jogados para dentro de um buraco negro próximo ' +
                    'de sua localização.',

                    'Kevin: Operador (a) ' + str(
                        username) + ' ,preciso de assistência, os malditos Krombs me jogaram para dentro de um buraco ' +
                    'negro e tem coisas estranhas aqui, responda. \n\n' + str(
                        username) + ': Kevin estou ciente de sua situação, isso que acontece quando você decide ' +
                    ' baixar sua guarda e tomar um pouco de sol... \n\nKevin: Me diga operador (a), que lugar é esse! Vejo livros e cadernos voando e também algumas ' +
                    'escrituras alienigenas que parecem palavras?!',

                    '' + str(
                        username) + ': Você parece estar no que chamamos de DIMENSÃO DA GRAMÁTICA. \nEssas escrituras' +
                    ' são na verdade palavras em português! \n\nOs krombs devem ser os responsáveis por criptografar essas palavras para que você não' +
                    ' fosse capaz de compreender.',

                    'O buraco negro possivelmente foi criado por eles para te prender nessa dimensão, sua única saída é coletar todas' +
                    ' as palavras que a dimensão te informar... \n\nKevin: E pensar que a tecnologia deles chegou a esse ponto...' +
                    '\n\nOperador vou precisar de sua ajuda nessa missão, me diga quais palavras devo coletar para que juntos possamos escapar daqui e acabar' +
                    ' com esses aliens!',

                    'Não importa onde vocês prendam a raça humana Krombs, nós somos inteligentes o suficiente para escapar de qualquer ' +
                    'lugar, especialmente de uma DIMENSÃO DA GRAMÁTICA... \n\nManda ver!']
    elif(tipo == "boss"):
        
        imagens = ['Images/cenarios/cenario9.png', 'Images/cenarios/cenario10.png','Images/cenarios/cenario10.png','Images/cenarios/cenario11.png', 'Images/cenarios/cenario11.png','Images/cenarios/cenario11.png']
    
        dialogos = ['Kevin: Parece que escapamos! Essa foi por pouco, Operador (a) ' + str(username) + '\n\n' +
                    'Espera... Aquilo é.. um Kromb!?' +'\n\n' +
                    'Kromb: Você é o primeiro humano que escapou de minha armadilha... Como recompensa vou revelar meu plano para vocês' +'\n\n' +
                    'Kevin: Hum... Okay? (Mas eu nem perguntei nada??)',

                    'Kromb: A raça de Krombs me escolheu como líder dessa missão por ser o mais inteligente e ser capaz de simular buracos negros.' +'\n\n'+
                    'Meus subordinados servem apenas como distração enquanto eu crio o buraco negro e então prendemos todos os pilotos humanos em seu pesadelo pessoal',

                    '' + str(username) + ': Espera um momento, pesadelo pessoal? Mas você prendeu Kevin na dimensão da gramática... Kevin?' +'\n\n'+
                    'Kevin: Hum... Eu detestava gramática ok?! Tenho trauma daquela época até hoje...' +'\n\n'+
                    'Kromb: Agora tudo faz sentido, a profecia Kromb diz que o mundo será nosso quando o português deixar de ser falado... Você! se você tivesse ficado preso naquela dimensão nós já teríamos o controle do universo!',

                    'Kevin: Essa nave Kromb, meus tiros fazem efeito operador(a) ' + str(username) +' ? \n\n'+
                    ''+ str(username)+': Não enquanto os escudos estiverem ativos.',
                    
                    'Mas eu tenho uma ideia,você percebeu que o buraco negro trouxe palavras da dimensão da gramática?' +'\n\n'+
                    'Podemos usar essas palavras como energia para gerar Nukes e quebrar o escudo do Kromb'+'\n\n'+
                    'Kromb: Hey chega de papo furado, chegou a hora dos Krombs dominarem o universo.',
                    
                    'Diga adeus a sua vida e a seu planeta!' +'\n\n'+
                    'Kevin: Here we go again...']
    else:

        imagens = ['Images/cenarios/cenario7.png', 'Images/cenarios/cenario8.png','Images/cenarios/cenario8.png']
    
        dialogos = ['[Falado na língua Kromb] Malditos Humanos! Noooooooo! \n\n' +
                    'KABOOOM!' ,

                    'Mais uma missão cumprida com sucesso, Operador(a) ' + str(username) +'\n\n'+
                    ''+ str(username) +': Como esperado de meu parceiro, agora você irá voltar para a base certo Kevin?'+'\n\n'+

                    'Quem eu? Não meu caro! O Sol ainda está ótimo preciso aproveitar haha',
                    
                    'Space Learners - Gramática de forma divertida' +'\n\n'+
                    'Fim']
        
    rodarHistoria(imagens, dialogos)
    
def menu(musica,efeitos_sonoros):
    sair = 0
    held = False
    w,h = 50,50
    x,y=0,0
    asteroides=[]
    
    #Background
    background_image_filename = 'Images/background/menu_image.png'
    background = pygame.image.load(background_image_filename).convert_alpha()

    #Sprites
    music_on_image_filename = music_on
    music_off_image_filename = music_off
        
    effects_on_image_filename = effects_on
    effects_off_image_filename = effects_off

    #Textos

    planet_font = pygame.font.Font(spaceFont2, 80) #Fonte para escrever na tela
    planet_text = planet_font.render('•', True, (255,205,0))

    logo_font = pygame.font.Font(spaceFont2, 30) #Fonte para escrever na tela    
    logo_text = logo_font.render('SPACE  LEARNERS', True, (0,255,0))

    user_text = logo_font.render('Bem vindo '+ str(username) + '!', True, (0,255,0))
    
    btn_font = pygame.font.SysFont(tahoma, 16, bold=True) #Fonte para escrever na tela
    
    btn_jogar_text = btn_font.render('Jogar', True, (0,255,0))

    btn_instruc_text = btn_font.render('Instruções', True, (0,255,0))

    btn_creditos_text = btn_font.render('Créditos', True, (0,255,0))

    btn_sair_text = btn_font.render('Sair', True, (0,255,0))

    #Sons
    btn_musica_text = btn_font.render('', True, (0,255,0))
    btn_efeitos_text = btn_font.render('', True, (0,255,0))
    
    #Retangulos dos Textos

    planet_Rect = logo_text.get_rect()  
    planet_Rect.center = (520,40)

    logo_Rect = logo_text.get_rect()  
    logo_Rect.center = (590,80)

    user_Rect = user_text.get_rect()  
    user_Rect.center = (410,520)

    btn_jogar_Rect = btn_jogar_text.get_rect()  
    btn_jogar_Rect.center = (600,165)
    botao_jogar_cor = (0,0,0)

    btn_instruc_Rect = btn_instruc_text.get_rect()  
    btn_instruc_Rect.center = (600,225)
    botao_instruc_cor = (0,0,0)

    btn_creditos_Rect = btn_creditos_text.get_rect()  
    btn_creditos_Rect.center = (600,285)
    botao_creditos_cor = (0,0,0)

    btn_sair_Rect = btn_sair_text.get_rect()  
    btn_sair_Rect.center = (600,345)
    botao_sair_cor = (0,0,0)

    #Sons

    btn_musica_Rect = btn_musica_text.get_rect()  
    btn_musica_Rect.center = (330,515)
    botao_musica_cor = (0,0,0)

    btn_efeitos_Rect = btn_efeitos_text.get_rect()  
    btn_efeitos_Rect.center = (400,515)
    botao_efeitos_cor = (0,0,0)

    btnMusica = Button(10,10,'musica')
    btnSom = Button(70,10,'som')

    while(sair == 0):
        x_draw,y_draw = 100,70
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x,y = pygame.mouse.get_pos()
                pos = (x,y)
                #Para ajustar o movimento (centralizar mouse com retangulo)
                x-=w/2
                y-=h/2
                if btnMusica.click(pos):
                    btnMusica.update()
                    if(musica == False):
                        musica=True
                    else:
                        musica=False
                if btnSom.click(pos):
                    btnSom.update()
                    if(efeitos_sonoros == False):
                        efeitos_sonoros=True
                    else:
                        efeitos_sonoros=False
            #Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held= True
            if event.type == MOUSEBUTTONUP:
                held = False


        #musica = btnMusica.musica
        #efeitos_sonoros = btnSom.musica
                
        #Musica
        if musica:
            pygame.mixer.music.unpause()
            btnMusica.sprite = pygame.image.load(music_on_image_filename).convert_alpha()
        else:
            pygame.mixer.music.pause()
            btnMusica.sprite = pygame.image.load(music_off_image_filename).convert_alpha()
            
        #Efeitos sonoros
        if efeitos_sonoros:
            btnSom.sprite = pygame.image.load(effects_on_image_filename).convert_alpha()
        else:
            btnSom.sprite = pygame.image.load(effects_off_image_filename).convert_alpha()
            
        screen.fill((255, 255, 255))

        #Background
        screen.blit(background, (0,0))

        #Gerar obstaculos como background
        if(len(asteroides) <6):
            obst_tamanho = random.randint(6,10)
            asteroides.append(Asteroide(obst_tamanho,0.1))

        #Desenhar asteroides
        for i in range(0,len(asteroides),1):
            screen.blit(asteroides[i].sprite, (asteroides[i].x-50,asteroides[i].y-50))

        #botão musica e som
        btnMusica.draw(screen)
        btnSom.draw(screen)
        
        #Desenhar logo e Username
        screen.blit(planet_text,planet_Rect) 
        screen.blit(logo_text, logo_Rect)

        #pygame.draw.rect(screen,(0,0,0),(180,485,440,70))
        screen.blit(user_text, user_Rect)
        
        #Botoes
        botao_jogar_rect = create_retangulo(500,150,200,30)
        pygame.draw.rect(screen, (0,255,0), botao_jogar_rect,3)
        pygame.draw.rect(screen, botao_jogar_cor, (500,150,200,30))
        screen.blit(btn_jogar_text, btn_jogar_Rect)

        botao_instruc_rect = create_retangulo(500,210,200,30)
        pygame.draw.rect(screen, (0,255,0), botao_instruc_rect,3)
        pygame.draw.rect(screen, botao_instruc_cor, (500,210,200,30))
        screen.blit(btn_instruc_text, btn_instruc_Rect)

        botao_creditos_rect = create_retangulo(500,270,200,30)
        pygame.draw.rect(screen, (0,255,0), botao_creditos_rect,3)
        pygame.draw.rect(screen, botao_creditos_cor, (500,270,200,30))
        screen.blit(btn_creditos_text, btn_creditos_Rect)

        botao_sair_rect = create_retangulo(500,330,200,30)
        pygame.draw.rect(screen, (0,255,0), botao_sair_rect,3)
        pygame.draw.rect(screen, botao_sair_cor, (500,330,200,30))
        screen.blit(btn_sair_text, btn_sair_Rect)

        #Movimentação dos asteroides
        for i in range (0,len(asteroides),1):
            asteroides[i].move()

        
        #Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:
        if(botao_jogar_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_jogar_cor = (255,255,255)
            sair = 1
        elif(botao_jogar_rect.collidepoint(pygame.mouse.get_pos())):
            botao_jogar_cor = (255,255,255)
        else:
            botao_jogar_cor = (0,0,0)

        if(botao_instruc_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_instruc_cor = (255,255,255)
            sair = 2
        elif(botao_instruc_rect.collidepoint(pygame.mouse.get_pos())):
            botao_instruc_cor = (255,255,255)
        else:
            botao_instruc_cor = (0,0,0)

        if(botao_creditos_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_creditos_cor = (255,255,255)
            sair = 3
        elif(botao_creditos_rect.collidepoint(pygame.mouse.get_pos())):
            botao_creditos_cor = (255,255,255)
        else:
            botao_creditos_cor = (0,0,0)
            
        if(botao_sair_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_sair_cor = (255,255,255)
            sair = -1
        elif(botao_sair_rect.collidepoint(pygame.mouse.get_pos())):
            botao_sair_cor = (255,255,255)
        else:
            botao_sair_cor = (0,0,0)
        
            
        pygame.display.update()
    return sair, musica, efeitos_sonoros

def instrucoesBase(background,tipoTela, ultima):
    sair = 0
    held = False
    w, h = 50, 50
    x, y = 0, 0
    btnText = 'Próximo'
    titulo = 'Controles'

    # Background
    background_image_filename = background
    background = pygame.image.load(background_image_filename).convert_alpha()

    # Textos
    controles_font = pygame.font.Font(spaceFont2, 25)  # Fonte para escrever na tela

    if(tipoTela!= 'Controles'):
        titulo = tipoTela

    controles_text = controles_font.render(titulo, True, (0, 255, 0))
    
    btn_font = pygame.font.SysFont(tahoma, 16, bold=True) #Fonte para escrever na tela

    if(ultima):
        btnText = 'Voltar ao Menu'
        
    btn_next_text = btn_font.render(btnText, True, (0, 255, 0))
    # Retangulos dos Textos
    controles_Rect = controles_text.get_rect()
    controles_Rect.center = (420, 90)

    btn_next_Rect = btn_next_text.get_rect()
    btn_next_Rect.center = (410, 370)
    botao_next_cor = (0, 0, 0)

    while (sair == 0):
        x_draw, y_draw = 100, 70
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x, y = pygame.mouse.get_pos()
                # Para ajustar o movimento (centralizar mouse com retangulo)
                x -= w / 2
                y -= h / 2
            # Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held = True
            if event.type == MOUSEBUTTONUP:
                held = False
                
        screen.fill((255, 255, 255))

        # Background
        screen.blit(background, (0, 0))

        #Titulo
        screen.blit(controles_text, controles_Rect) 
        
        # Botoes
        botao_next_rect = create_retangulo(310, 355, 200, 30)
        pygame.draw.rect(screen, (0, 255, 0), botao_next_rect, 3)
        pygame.draw.rect(screen, botao_next_cor, (310, 355, 200, 30))
        screen.blit(btn_next_text, btn_next_Rect)

        # Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:

        if (botao_next_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_next_cor = (255, 255, 255)
            sair = -1
        elif (botao_next_rect.collidepoint(pygame.mouse.get_pos())):
            botao_next_cor = (255, 255, 255)
        else:
            botao_next_cor = (0, 0, 0)
            # carregar proxima tela

        pygame.display.update()

    while (sair == 0):
        x_draw, y_draw = 100, 70
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x, y = pygame.mouse.get_pos()
                # Para ajustar o movimento (centralizar mouse com retangulo)
                x -= w / 2
                y -= h / 2
            # Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held = True
            if event.type == MOUSEBUTTONUP:
                held = False

        screen.fill((255, 255, 255))

        # Background
        screen.blit(background, (0, 0))

        # Titulo
        screen.blit(controles_text, controles_Rect)

        # Botoes
        botao_next_rect = create_retangulo(250, 510, 300, 50)
        pygame.draw.rect(screen, (0, 255, 0), botao_next_rect, 3)
        pygame.draw.rect(screen, botao_next_cor, (250, 510, 300, 50))
        screen.blit(btn_next_text, btn_next_Rect)

        # Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:

        if (botao_next_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_next_cor = (255, 255, 255)
            sair = -1
        elif (botao_next_rect.collidepoint(pygame.mouse.get_pos())):
            botao_next_cor = (255, 255, 255)
        else:
            botao_next_cor = (0, 0, 0)
            # carregar proxima tela

        pygame.display.update()

    return sair



def instrucoes_controles():
    instrucoesBase('Images/background/controle.png','Controles', False)
    
def instrucoes_jogo():
    instrucoesBase('Images/background/dicas.png','Dicas', False)
    

def instrucoes_interface():
    instrucoesBase('Images/background/interface.png','Interface', False)

def instrucoes_powerups():
    instrucoesBase('Images/background/powerups.png','Power Ups', True)

def creditos():
    instrucoesBase('Images/background/creditos.png','Créditos', True)
    

def rankingPontos(teste,score):
    sair = 0
    held = False
    w, h = 50, 50
    x, y = 0, 0

    # Background
    background_image_filename = 'Images/background/background5.png'
    background = pygame.image.load(background_image_filename).convert_alpha()

    # Textos
    logo_font = pygame.font.Font(spaceFont2, 20)  # Fonte para escrever na tela
    logo_text = logo_font.render('R A N K I N G ', True, (0, 255, 0))
    text_font = pygame.font.Font(spaceFont2, 15)
    if teste:
        user_text = text_font.render('Sua pontuação entra no TOP 10!! Foi: ' + str(score) + '  ', True, (0, 255, 0))
    else:
        user_text = text_font.render('Não é TOP 10, Pontos: ' + str(score) + '  ', True, (0, 255, 0))
    btn_font = pygame.font.Font(spaceAdventure, 14)  # Fonte para escrever na tela

    l = lerScore()
    i=1
    msg = []
    for x in l:
        msg.append(str(i) +  ' - Nome: ' + str(x.get_nome()) + ' //  Pontos: ' + str(x.get_pontos()) )
        i += 1

    ranking_text = []
    ranking_Rect = []
    for x in range(0,10,1):
        ranking_text.append(text_font.render(msg[x], True, (0, 255, 0)))
        ranking_Rect.append(ranking_text[x].get_rect())
        ranking_Rect[x].center = (400, 130+(x*25))

    btn_sair_text = btn_font.render('Sair', True, (0, 255, 0))

    # Retangulos dos Textos



    logo_Rect = logo_text.get_rect()
    logo_Rect.center = (410, 80)

    user_Rect = user_text.get_rect()
    user_Rect.center = (410, 420)


    btn_sair_Rect = btn_sair_text.get_rect()
    btn_sair_Rect.center = (400, 525)
    botao_sair_cor = (0, 0, 0)

    while (sair == 0):
        x_draw, y_draw = 100, 70
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x, y = pygame.mouse.get_pos()
                # Para ajustar o movimento (centralizar mouse com retangulo)
                x -= w / 2
                y -= h / 2
            # Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held = True
            if event.type == MOUSEBUTTONUP:
                held = False

        screen.fill((255, 255, 255))

        # Background
        screen.blit(background, (0, 0))

        ret1 = create_retangulo(160, 40, 500, 440)
        ret2 = create_retangulo(180, 60, 460, 400)
        pygame.draw.rect(screen, (0, 255, 0), ret1)
        pygame.draw.rect(screen, (0, 0, 0), ret2)

        # Desenhar logo e Username
        for x in range(0,10,1):
            screen.blit(ranking_text[x], ranking_Rect[x])
        screen.blit(logo_text, logo_Rect)
        screen.blit(user_text, user_Rect)
        # Botoes

        botao_sair_rect = create_retangulo(250, 500, 300, 50)
        pygame.draw.rect(screen, (0, 255, 0), botao_sair_rect, 3)
        pygame.draw.rect(screen, botao_sair_cor, (250, 500, 300, 50))
        screen.blit(btn_sair_text, btn_sair_Rect)

        # Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:

        if (botao_sair_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_sair_cor = (255, 255, 255)
            sair = -1
        elif (botao_sair_rect.collidepoint(pygame.mouse.get_pos())):
            botao_sair_cor = (255, 255, 255)
        else:
            botao_sair_cor = (0, 0, 0)
            # carregar proxima tela

        pygame.display.update()
    return sair

def escolher_cor_nave():
    sair = False
    voltar = False
    w,h = 50,50
    cores = [(255,0,0),(255,0,255),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(0,0,0),(255,165,0),(0,100,0)]
    dialogos = ["Uma cor clássica!","Não é muito meu estilo,\nmas ok","Me sinto jogando como \nLuigi","Boa escolha operador","Amarelo bacana","Ciano Top","Realmente parece a \nBatwing","Laranja muito bom","Um verde para os fortes"]
    retangulos = []
    cor_nave = (255,0,0)
    x,y=0,0
    held = False

    #Background
    background_image_filename = 'Images/background/fundo2.jpg'
    background = pygame.image.load(background_image_filename).convert_alpha()


    #Sprites
    kevin = pygame.image.load(kevin_sprite).convert_alpha()

    #Criando fontes e textos
    game_font = pygame.font.Font(spaceAdventure, 24) #Fonte para escrever na tela
    text = game_font.render('Escolha a cor da nave USS Galactica', True, (0,255,0))

    btn_font = pygame.font.SysFont(tahoma, 16, bold=True) #Fonte para escrever na tela
    btn_text = btn_font.render('Pronto!', True, (0,255,0))

    btnVoltar_text = btn_font.render('Voltar ao Menu', True, (0,255,0))
    
    #Ajustando caixas de texto
    textRect = text.get_rect()  
    textRect.center = (400,30)

    btnRect = btn_text.get_rect()  
    btnRect.center = (660,525)
    botao_cor = (0,0,0)

    btnVoltarRect = btnVoltar_text.get_rect()  
    btnVoltarRect.center = (140,525)
    botaoVoltar_cor = (0,0,0)
    
    #Mensagem default sobre a cor da nave
    mensagem = dialogos[0]
    dialogo_size = 16

    #Sprite Nave
    nave_image_filename = nave_vermelha
    nave_sprite = pygame.image.load(nave_image_filename).convert_alpha()

    while(sair == False):
        x_draw,y_draw = 200,100
        game_font2 = pygame.font.SysFont(tahoma, 18,bold=True) #Fonte para escrever na tela
        dialogo = game_font2.render(mensagem, True, (0,255,0), (0,0,0))
        dialogoRect = dialogo.get_rect() 
        dialogoRect.center = (460,380)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x,y = pygame.mouse.get_pos()
                #Para ajustar o movimento (centralizar mouse com retangulo)
                x-=w/2
                y-=h/2
            #Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held= True
            if event.type == MOUSEBUTTONUP:
                held = False
                
        screen.fill((255, 255, 255))

        #Background
        screen.blit(background, (0,0))
        
        #Escreve texto para escolher nave na tela
        screen.blit(text, textRect) 
        
        #Cria e desenha os retangulos para escolher a cor da nave
        pygame.draw.rect(screen, (255,255,255), (190,90,210,210)) 
        pygame.draw.rect(screen, (0,255,0), (190,90,210,210),3)
        
        for i in range(0,9,1):
            retangulos.append(create_retangulo(x_draw,y_draw,w,h))
            pygame.draw.rect(screen,(cores[i]),retangulos[i]) #define retangulo
            x_draw+=70
            if((i+1)%3 == 0): #3 retangulos por linha
                x_draw=200
                y_draw+=70
                
        pygame.draw.rect(screen, (255,255,255), (500,190,100,100)) #Nave
        pygame.draw.rect(screen, (0,255,0), (500,190,100,100),3)
        screen.blit(nave_sprite , (500,190,100,100))

        #Desenhar objetos de dialogo
        pygame.draw.rect(screen, (0,0,0), (190,330,410,120))
        pygame.draw.rect(screen, (0,255,0), (190,330,130,120),3)
        screen.blit(kevin, (200,340 )) #desenha sprite na posicao
        #Desenhar dialogo
        blit_text(screen, mensagem, (350,360),game_font2)
        pygame.draw.rect(screen, (0,255,0), (190,330,410,120),3)

        botao_rect = create_retangulo(560,500,200,50)
        pygame.draw.rect(screen, (0,255,0), botao_rect,3)
        pygame.draw.rect(screen, botao_cor, (560,500,200,50))
        screen.blit(btn_text, btnRect)

        botaoVoltar_rect = create_retangulo(40,500,200,50)
        pygame.draw.rect(screen, (0,255,0), botaoVoltar_rect,3)
        pygame.draw.rect(screen, botaoVoltar_cor, (40,500,200,50))
        screen.blit(btnVoltar_text, btnVoltarRect)
        
        #Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:
        for i in range(0,9,1):
            if (retangulos[i].collidepoint(pygame.mouse.get_pos()) and held):
                cor_nave = cores[i] #trocar por sprite da nave
                #Sprite Nave
                if(i == 0):
                    nave_image_filename = nave_vermelha
                elif(i == 1):
                     nave_image_filename = nave_rosa
                elif(i == 2):
                     nave_image_filename = nave_verde
                elif(i == 3):
                     nave_image_filename = nave_azul_escura
                elif(i == 4):
                     nave_image_filename = nave_amarela
                elif(i == 5):
                     nave_image_filename = nave_azul
                elif(i == 6):
                     nave_image_filename = nave_preta
                elif(i == 7):
                     nave_image_filename = nave_laranja
                else:
                     nave_image_filename = nave_verde_escura
                nave_sprite = pygame.image.load(nave_image_filename).convert_alpha()
                #Alterar Texto
                mensagem = dialogos[i]

        #Botoes

        if(botao_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_cor = (255,255,255)
            sair = True
        elif(botao_rect.collidepoint(pygame.mouse.get_pos())):
            botao_cor = (255,255,255)
        else:
           botao_cor = (0,0,0)
            #carregar proxima tela

        if(botaoVoltar_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botaoVoltar_cor = (255,255,255)
            sair = True
            voltar = True
        elif(botaoVoltar_rect.collidepoint(pygame.mouse.get_pos())):
            botaoVoltar_cor = (255,255,255)
        else:
           botaoVoltar_cor = (0,0,0)
            #carregar proxima tela
            
        pygame.display.update()

    return nave_image_filename, voltar


def nivel(nave_sprite,dificuldade,background_nivel):
    sair = False
    w,h = 30,30
    x,y=0,0
    estado_jogo = "game over"
    obstaculos = 3
    #Criando fontes e textos
    pontos_font = pygame.font.Font(spaceAdventure, 14) #Fonte para escrever na tela

    #Background
    background_image_filename = background_nivel
    background = pygame.image.load(background_image_filename).convert_alpha()


    #Sprites
    kevin = pygame.image.load(kevin_sprite).convert_alpha()

    nave_sprite = pygame.image.load(nave_sprite).convert_alpha()

    sprite_bullet = pygame.image.load(bullet_sprite).convert_alpha()

    vida_sprite = pygame.image.load(vida).convert_alpha()

    nextlevel = pygame.image.load(next_level_sprite).convert_alpha()
    
    #criar objeto Nave
    nave = Nave(nave_sprite,400,550)
    increm_x = 0
    increm_y = 0
    vidas = []
    #ordem das palavras
    banco = bancodeFases(dificuldade)
    sorteio = random.randint(0,len(banco)-1)
    aux = banco[sorteio]
    if dificuldade!=3:
        velocidade = 1
    else:
        velocidade = 2
    fase = Fase(aux.ordem,aux.frase,velocidade)
    del(banco[sorteio])
    if dificuldade==1:
        numAste = 7
        obstaculos = 2
    elif dificuldade==2:
        numAste = 9
        obstaculos = 3
    else:
        numAste = 9
        obstaculos = 4

       
    #tempo por fase
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 1000)


    #Balas
    bullets =[]
    #Asteroides/Palavras
    asteroides = []
    limite_powerup = 0
    fpsClock = pygame.time.Clock()
    while(sair == False):
        x_draw,y_draw = 760,560 #posicao sprite de vidas
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            #Movimentando a nave
            #Evento KeyDown
            if event.type == KEYDOWN:
                if event.key==K_LEFT:
                    increm_x+=-10
                if event.key==K_RIGHT:
                    increm_x+=10
                if event.key==K_UP:
                    increm_y+=-10
                if event.key==K_DOWN:
                    increm_y+=10
                if event.key == pygame.K_SPACE:
                    if(efeitos_sonoros == True):
                        pygame.mixer.Channel(2).set_volume(0.008)
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound('Audio/tiro.wav'), maxtime=600)
                    bullet1 = Bullet(sprite_bullet,nave.x-45,nave.y)
                    bullet2 = Bullet(sprite_bullet,nave.x+5,nave.y)
                    bullets.append(bullet1)
                    bullets.append(bullet2)
                    if not fase.existePowerUp:
                        receberTeste = testePowerup()
                        if receberTeste:
                            fase.existePowerUp = True
                            op = random.randint(0,3)
                            fase.powerup = PowerUp(op)
                if event.key == K_p:
                    if(nave.powerup != "none"):
                        limite_powerup = powerup_release(nave.powerup,asteroides)
                        nave.powerup = "none"
            #Evento KeyUp
            if event.type == KEYUP:
                if event.key==K_LEFT or event.key == K_RIGHT:
                    increm_x=0
                if event.key==K_UP or event.key == K_DOWN:
                    increm_y=0

            if event.type == CLOCKTICK:
                if(fase.estado=='rolando'):
                    fase.tempo = fase.tempo - 1

        #Cria os obstaculos a cada frame em quantidades aleatorias
        if(len(asteroides) <numAste and limite_powerup <= 0):
            obst_tamanho = random.randint(0,obstaculos)
            asteroides.append(Asteroide(obst_tamanho,fase.nivel))
        elif (limite_powerup > 0):
            limite_powerup -= 1 
            if(limite_powerup <=0):
                normalizaVelocidade(asteroides)

        #Sistema de Spawn da Nave
        if nave.estado == 'spawn':
            nave.estado = 'nascendo'
            nave.tempospawn = 60
            nave.sprite = pygame.image.load(nave_spawn).convert_alpha()

        if nave.tempospawn < 0:
            nave.estado='jogando'
            nave.sprite = nave_sprite
        else:
            nave.tempospawn -=1



        nave.move(increm_x,increm_y)
        nave.update()
        screen.fill((255, 255, 255))
        screen.blit(background, (0,0))
        screen.blit(nave.sprite, (nave.x-50,nave.y-50))
        #pygame.draw.circle(screen, (255, 0, 0), (nave.circulo.x, nave.circulo.y), nave.raio, 1) DESCOMENTAR

        #powerup caso exista
        if fase.existePowerUp:
            fase.powerup.move()
            fase.powerup.draw(screen)
            if fase.powerup.colisaoComNave(nave):
                if fase.powerup.tipo=='1up':
                    nave.ganhaVida()
                else:
                    nave.powerup = fase.powerup.tipo
                fase.powerup = ''
                fase.existePowerUp = False

        #Desenhar asteroides
        for i in range(0,len(asteroides),1): #DESCOMENTAR
            #pygame.draw.circle(screen, (255,0,0), (asteroides[i].circulo.x, asteroides[i].circulo.y), asteroides[i].circulo.r, 1)
            screen.blit(asteroides[i].sprite, (asteroides[i].x-50,asteroides[i].y-50))

        #Remove todos os asteroides vermelhos (que colidiram na iteração anterior) Explosao
        for asteroide in asteroides:
            if(asteroide.colisao == True):
                asteroides.remove(asteroide)


        #Desenhar Interface - pontos
        pontos_text = pontos_font.render("Pontos: "+str(nave.pontos), True, (0,255,0))
        pontosRect = pontos_text.get_rect()
        pontosRect.center = (700,10)
        screen.blit(pontos_text, pontosRect)

        #para ganhar vidas
        if(nave.pontos > fase.pontospravida):
            nave.ganhaVida()
            fase.pontospravida += 5000

        #Desenhar Interface - vidas
        for i in range(0,nave.vidas,1):
            vidas.append(Vida(x_draw,y_draw))
            screen.blit(vida_sprite, (vidas[i].x, vidas[i].y))
            x_draw-=40

        pygame.draw.rect(screen, (0, 255, 0), (10, 520, 50, 70))  
        pygame.draw.rect(screen, (0, 0, 0), (15, 525, 40, 60))
        desenharPowerUp(nave.powerup)

        #Checar colisões para que sejam removidos na proxima iteração
        for i in range(0,len(asteroides),1):
            for j in range(0,len(asteroides),1):
                if(i!=j):
                    colidiu = colisao(asteroides[i],asteroides[j])
            for j in bullets:
                colidiu = colisaoBala(j,asteroides[i])
                if colidiu == True:
                    nave.pontos += 100

            colidiu = colisaoNaveAsteroide(nave,asteroides[i])
            if colidiu:
                #tocar audio
                #if(efeitos_sonoros == True):
                    #pygame.mixer.Channel(3).play(pygame.mixer.Sound('Audio/perde_vida.wav'), maxtime=600)
                nave.perdeVida()
                nave.estado = 'spawn'


        #movimentação das palavras
        fase.draw(screen)
        fase.update()
        fase.testarOrdem()
        for i in fase.ordem:
            if not i.colidiu:
                if i.colisaoNavePalavra(nave):
                    fase.ordemJogador.append(i.texto)
                    i.colidiu = True

        #Teste Game Over
        if(nave.vidas == 0 or fase.estado=='perdida'):
            estado_jogo = "game over"
            sair = True

        #teste do fim de fase
        if fase.estado=='acertou':
            if fase.contador != 2:
                sorteio = random.randint(0, len(banco)-1)
                aux = banco[sorteio]
                del (banco[sorteio])
                fase.ordem = cria_palavras(aux.ordem)
                fase.frase = aux.frase
                fase.resetFase()
                fase.contador+=1
                nave.pontos +=800
            elif fase.contador==2:
                portal = Portal(nextlevel)
                portal.draw(screen)
                if portal.colisao(nave):
                    nave.pontos+= 2000
                    estado_jogo = "nivel completo"
                    sair = True
        elif fase.estado=='errou':
            t = pygame.time.get_ticks()
            temponovo = t
            fase.estado='reiniciando'
            nave.pontos -= 200
        elif fase.estado == 'reiniciando':
            temponovo+=9
            if t+1000 < temponovo:
                 fase.resetFase()

        #Movimentação dos asteroides
        for i in range (0,len(asteroides),1):
            asteroides[i].move()

        #Movimentar balas ate sairem da cena
        for i in range(0, len(bullets) , 1):
            if i<len(bullets):
                if not bullets[i].colisao:
                    bullets[i].move()
                    if(bullets[i].y < 0):
                        bullets.remove(bullets[i])
                    else:
                        screen.blit(bullets[i].sprite, (bullets[i].x-20,bullets[i].y-20)) 
                else:
                    bullets.remove(bullets[i])
        #Impedir nave de sair da tela


        #atualiza a janela
        pygame.display.update()
        fpsClock.tick(FPS)


        
    return estado_jogo, nave.pontos,fase.tempo

def telaNivelCompleto(score,tempo):
    sair = 0
    held = False
    w,h = 50,50
    x,y=0,0
    tempo*=10
    
    #Background
    background_image_filename = 'Images/background/fundo3.jpg'
    background = pygame.image.load(background_image_filename).convert_alpha()

    #Textos

    titulo_font = pygame.font.Font(spaceAdventure, 30) 
    titulo_text = titulo_font.render('Nivel Completo!', True, (0,255,0))

    textos_font = pygame.font.SysFont(arial, 18, bold=True)
    player_text = textos_font.render('Jogador (a): '+str(username), True, (0,255,0))
    score_text = textos_font.render('Pontos: '+str(score), True, (0,255,0))
    tempo_text = textos_font.render('Tempo: '+str(tempo), True, (0,255,0))

    btn_font = pygame.font.SysFont(arial, 14, bold=True)
    btn_next_text = btn_font.render('Próximo Nível', True, (0,255,0))

    
    #Retangulos dos Textos

    titulo_Rect = titulo_text.get_rect()  
    titulo_Rect.center = (410,140)

    player_Rect = player_text.get_rect()  
    player_Rect.center = (410,220)

    score_Rect = score_text.get_rect()  
    score_Rect.center = (355,270)

    tempo_Rect = tempo_text.get_rect()  
    tempo_Rect.center = (355,320)

    btn_next_Rect = btn_next_text.get_rect()  
    btn_next_Rect.center = (400,465)
    botao_next_cor = (0,0,0)
    
    while(sair == 0):

        score_text = textos_font.render('Pontos: '+str(score), True, (0,255,0))
        if(tempo < 0):
            tempo_text = textos_font.render('Tempo: Limite Atingido!', True, (0,255,0))
        else:
            tempo_text = textos_font.render('Tempo: '+str(tempo), True, (0,255,0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x,y = pygame.mouse.get_pos()
                #Para ajustar o movimento (centralizar mouse com retangulo)
                x-=w/2
                y-=h/2
            #Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held= True
            if event.type == MOUSEBUTTONUP:
                held = False

        screen.fill((255, 255, 255))

        #Background
        screen.blit(background, (0,0))

        #Desenhar retangulo para colocar as informacoes
        ret1 = create_retangulo(210,100,400,440)
        ret2 = create_retangulo(230,120,360,400)
        pygame.draw.rect(screen, (0,255,0),ret1)
        pygame.draw.rect(screen, (0,0,0),ret2)

        
        #Desenhar Titulo
        screen.blit(titulo_text, titulo_Rect) 

        #Player, score, tempo
        screen.blit(player_text, player_Rect)
        screen.blit(score_text, score_Rect)
        screen.blit(tempo_text, tempo_Rect)

        #Botao Next
        botao_next_rect = create_retangulo(300,440,200,50)
        pygame.draw.rect(screen, (0,255,0), botao_next_rect,3)
        pygame.draw.rect(screen, botao_next_cor, botao_next_rect)
        screen.blit(btn_next_text, btn_next_Rect)

        #Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:
        if(botao_next_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_next_cor = (255,255,255)
            sair = 1
        elif(botao_next_rect.collidepoint(pygame.mouse.get_pos())):
            botao_next_cor = (255,255,255)
        else:
            botao_next_cor = (0,0,0)

        #Transformar tempo em pontos por frame:
        if(tempo >0):
            score +=10
            tempo -= 1
            if(tempo <=0):
                tempo = 0
            
        #carregar proxima tela
            
        pygame.display.update()
        
    return score

def telaGameOver(scoreTotal,tempoTotal,niveisCompletos):
    sair = 0
    held = False
    w,h = 50,50
    x,y=0,0
    
    #Background
    background_image_filename = 'Images/background/fundo4.jpg'
    background = pygame.image.load(background_image_filename).convert_alpha()

    #Textos

    titulo_font = pygame.font.Font(spaceAdventure, 30) 
    titulo_text = titulo_font.render('Game Over', True, (255,0,0))

    textos_font = pygame.font.SysFont(arial, 18, bold=True)
    player_text = textos_font.render('Jogador (a): '+str(username), True, (255,0,0))
    score_text = textos_font.render('Pontuação Final: '+str(scoreTotal), True, (255,0,0))
    tempo_text = textos_font.render('Tempo Total: '+str(tempoTotal) +" segundos", True, (255,0,0))
    niveis_text = textos_font.render('Níveis Completos: '+str(niveisCompletos), True, (255,0,0))

    btn_font = pygame.font.SysFont(arial, 14, bold=True)
    btn_menu_text = btn_font.render('Voltar ao Menu', True, (255,0,0))

    
    #Retangulos dos Textos

    titulo_Rect = titulo_text.get_rect()  
    titulo_Rect.center = (400,160)

    player_Rect = player_text.get_rect()  
    player_Rect.center = (400,220)

    score_Rect = score_text.get_rect()  
    score_Rect.center = (365,270)

    tempo_Rect = tempo_text.get_rect()  
    tempo_Rect.center = (390,320)

    niveis_Rect = tempo_text.get_rect()  
    niveis_Rect.center = (390,370)

    btn_menu_Rect = btn_menu_text.get_rect()  
    btn_menu_Rect.center = (400,465)
    botao_menu_cor = (0,0,0)
    if(musica == True):
        pygame.mixer.Channel(2).set_volume(0.008)
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('Audio/game_over.wav'))
    
    while(sair == 0):
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if held:
                x,y = pygame.mouse.get_pos()
                #Para ajustar o movimento (centralizar mouse com retangulo)
                x-=w/2
                y-=h/2
            #Movimentando
            if event.type == MOUSEBUTTONDOWN:
                held= True
            if event.type == MOUSEBUTTONUP:
                held = False

        screen.fill((255, 255, 255))

        #Background
        screen.blit(background, (0,0))

        #Desenhar retangulo para colocar as informacoes
        ret1 = create_retangulo(210,100,400,440)
        ret2 = create_retangulo(230,120,360,400)
        pygame.draw.rect(screen, (255,0,0),ret1)
        pygame.draw.rect(screen, (0,0,0),ret2)

        
        #Desenhar Titulo
        screen.blit(titulo_text, titulo_Rect) 

        #Player, score, tempo
        screen.blit(player_text, player_Rect)
        screen.blit(score_text, score_Rect)
        screen.blit(tempo_text, tempo_Rect)
        screen.blit(niveis_text, niveis_Rect)

        #Botao Next
        botao_menu_rect = create_retangulo(300,440,200,50)
        pygame.draw.rect(screen, (255,0,0), botao_menu_rect,3)
        pygame.draw.rect(screen, botao_menu_cor, botao_menu_rect)
        screen.blit(btn_menu_text, btn_menu_Rect)

        #Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:
        if(botao_menu_rect.collidepoint(pygame.mouse.get_pos()) and held):
            botao_menu_cor = (255,255,255)
            sair = 1
        elif(botao_menu_rect.collidepoint(pygame.mouse.get_pos())):
            botao_menu_cor = (255,255,255)
        else:
            botao_menu_cor = (0,0,0)

        #carregar proxima tela
            
        pygame.display.update()

def Boss(nave_sprite):
    sair = False
    w,h = 30,30
    x,y=0,0
    estado_jogo = "game over"
    dificuldade = 4
    usou = False
    
    if(musica == True):
        pygame.mixer.music.load('Audio/boss_theme.wav')
        pygame.mixer.music.set_volume(0.02)
        pygame.mixer.music.play(loops=-1) 
    
    #Criando fontes e textos
    pontos_font = pygame.font.Font(spaceAdventure, 14) #Fonte para escrever na tela

    #Background
    background_image_filename = 'Images/background/final_boss.png'
    background = pygame.image.load(background_image_filename).convert_alpha()

    #Sprites

    nave_sprite = pygame.image.load(nave_sprite).convert_alpha()

    sprite_bullet = pygame.image.load(bullet_sprite).convert_alpha()

    vida_sprite = pygame.image.load(vida).convert_alpha()

    kromb_sprite = pygame.image.load(kromb_sprite1).convert_alpha()


    #criar objeto Nave
    nave = Nave(nave_sprite,400,550)
    increm_x = 0
    increm_y = 0
    vidas = []

    #Boss
    kromb = Kromb(kromb_sprite,400,100)
    
    #ordem das palavras
    banco = bancodeFases(dificuldade)
    sorteio = random.randint(0,len(banco)-1)
    aux = banco[sorteio]
    fase = Fase(aux.ordem,aux.frase,dificuldade)
    del(banco[sorteio])
    fase.faseBoss = True
    fase.tempo = 0
    #Balas
    bullets =[]
    velocidadebomba = 2
    #Asteroides/Palavras
    asteroides = []
    limite_powerup = 0
    dropbomb = 50
    fpsClock = pygame.time.Clock()
    increm = 1
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 1000)
    while(sair == False):
        x_draw,y_draw = 760,560 #posicao sprite de vidas
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            #Movimentando a nave
            #Evento KeyDown
            if event.type == KEYDOWN:
                if event.key==K_LEFT:
                    increm_x+=-12
                if event.key==K_RIGHT:
                    increm_x+=12
                if event.key==K_UP:
                    increm_y+=-12
                if event.key==K_DOWN:
                    increm_y+=12
                if event.key == pygame.K_SPACE:
                    if(efeitos_sonoros == True):
                        pygame.mixer.Channel(2).set_volume(0.008)
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound('Audio/tiro.wav'), maxtime=600)
                    bullet1 = Bullet(sprite_bullet,nave.x-45,nave.y)
                    bullet2 = Bullet(sprite_bullet,nave.x+5,nave.y)
                    bullets.append(bullet1)
                    bullets.append(bullet2)
                #Não gera mais PowerUps nesse level 
                if event.key == K_p:
                    if(nave.powerup != "none"):
                        limite_powerup = powerup_release(nave.powerup,asteroides)
                        if(nave.powerup == "nuke"):
                            kromb.estado = "machucado" #Alien vulneravel a ataques
                            usou = True
                        nave.powerup = "none"
            #Evento KeyUp
            if event.type == KEYUP:
                if event.key==K_LEFT or event.key == K_RIGHT:
                    increm_x=0
                if event.key==K_UP or event.key == K_DOWN:
                    increm_y=0
            if event.type == CLOCKTICK:
                    fase.tempo += 1
        #Muda sprite do Kromb de acordo com estado:
        if(kromb.estado =="atacando"):
            kromb.sprite = pygame.image.load(kromb_sprite_shield).convert_alpha()
            g = pygame.time.get_ticks()
            if g % dropbomb == 0:
                obst_tamanho = 5
                bomba = Asteroide(obst_tamanho, velocidadebomba)
                # Coloca posicao como X e Y da nave Kromb
                asteroides.append(bomba)
                bomba.x = kromb.x
                bomba.y = kromb.y + 50 + 20
        else:
            if(kromb.frameDano == 1):
                kromb.sprite = pygame.image.load(kromb_sprite_damaged).convert_alpha()
                kromb.frameDano = 0
            else:
                kromb.sprite = pygame.image.load(kromb_sprite2).convert_alpha()
            limite_powerup -= 1
            if(limite_powerup <=0):
                normalizaVelocidade(asteroides)
                kromb.estado ="atacando" #Kromb volta a atacar
                

        #VELOCIDADE DO KROMB
        if kromb.vida<100 and kromb.estadovida=='machucado':
            kromb.vx *= 2.5
            kromb.estadovida = 'morrendo'
            dropbomb = 40
        elif kromb.vida<200 and kromb.estadovida=='cheia':
            kromb.vx *= 4
            kromb.estadovida='machucado'
            dropbomb = 45

        #Sistema de spawn 
        if nave.estado == 'spawn':
            nave.estado = 'nascendo'
            nave.tempospawn = 15
            nave.sprite = pygame.image.load(nave_spawn).convert_alpha()

        if nave.tempospawn < 0:
            nave.estado='jogando'
            nave.sprite = nave_sprite
        else:
            nave.tempospawn -=1
        

        nave.move(increm_x,increm_y)
        nave.update()
        screen.fill((255, 255, 255))
        screen.blit(background, (0,0))
        screen.blit(nave.sprite, (nave.x-50,nave.y-50))
    
        #powerup caso exista (somente Nukes)
        if fase.existePowerUp:
            fase.powerup.move()
            fase.powerup.draw(screen)
            if fase.powerup.colisaoComNave(nave):
                nave.powerup = fase.powerup.tipo
                fase.powerup = ''
                fase.existePowerUp = False

        #Desenhar Kromb
        screen.blit(kromb.sprite, (int(kromb.x-75),int(kromb.y-75)))
        if fase.tempo == 400 :
            kromb.vx *= 1.02
            dropbomb = 10

        # Remove todos os asteroides vermelhos (que colidiram na iteração anterior) Explosao
        for asteroide in asteroides:
            asteroide.move()
            if (asteroide.colisao == True):
                asteroides.remove(asteroide)

        #Desenhar asteroides
        for i in range(0,len(asteroides),1):
            screen.blit(asteroides[i].sprite, (int(asteroides[i].x-14),int(asteroides[i].y-20))) #bombas
   

        #Desenhar Interface - pontos
        pontos_text = pontos_font.render("Pontos: "+str(nave.pontos), True, (0,255,0))
        pontosRect = pontos_text.get_rect()
        pontosRect.center = (700,10)
        screen.blit(pontos_text, pontosRect)


        #Desenhar Interface - vidas Nave
        for i in range(0,nave.vidas,1):
            vidas.append(Vida(x_draw,y_draw))
            screen.blit(vida_sprite, (vidas[i].x, vidas[i].y))
            x_draw-=40

        pygame.draw.rect(screen, (0, 255, 0), (10, 520, 50, 70))  # define retangulo
        pygame.draw.rect(screen, (0, 0, 0), (15, 525, 40, 60))
        desenharPowerUp(nave.powerup)

        #Desenhar Interface - vida Kromb
        pygame.draw.rect(screen, (255, 0, 0), (int(kromb.x-150), int(kromb.y+65), 300, 15)) #Dano recebido
        pygame.draw.rect(screen, (0, 255, 0), (int(kromb.x-150), int(kromb.y+65), kromb.vida, 15)) #Vida restante
        
        
        #Checar colisões para que sejam removidos na proxima iteração
        for i in range(0,len(asteroides),1):
            for j in bullets:
                colidiu = colisaoBala(j,asteroides[i])
                if colidiu == True:
                    nave.pontos += 50
            colidiu = colisaoNaveAsteroide(nave,asteroides[i])

            if colidiu:
                nave.perdeVida()
                nave.estado = 'spawn'

        if nave.estado=='jogando':
            colidiu_kromb = colisaoNaveAsteroide(nave, kromb)  # colisao com Kromb
            kromb.sprite = pygame.image.load(kromb_sprite1).convert_alpha()
            if colidiu_kromb:
                nave.perdeVida()
                nave.estado = 'spawn'

        #Checar colisao Kromb com balas:
        for b in bullets:
            colidiu = colisaoBala(b,kromb)
            kromb.sprite = pygame.image.load(kromb_sprite1).convert_alpha()
            if colidiu == True and kromb.estado!="atacando":
                nave.pontos += 50
                kromb.perdeVida()
                kromb.frameDano = 1
                
        #movimentação das palavras
        fase.draw(screen)
        fase.update()
        fase.testarOrdem()
        for i in fase.ordem:
            if not i.colidiu:
                if i.colisaoNavePalavra(nave):
                    fase.ordemJogador.append(i.texto)
                    i.colidiu = True

        #Teste Game Over
        if(nave.vidas == 0 or fase.estado=='perdida'):
            estado_jogo = "game over"
            sair = True

        #teste do fim de fase
        if kromb.vida <= 0:
                    estado_jogo = "nivel completo"
                    sair = True
                    
        if fase.estado=='acertou':
            font = pygame.font.SysFont(tahoma, 16,bold=True)  # Fonte para escrever na tela
            #Acertar uma frase impacta ganhar uma Nuke para destruir os escudos do Kromb
            if(usou == False):
                nave.powerup = 'nuke'
            msg = 'Você acertou!!! Agora use a nuke e atire no Kromb!!'
            text = font.render(msg, False, (0, 255, 0), (0, 0, 0))
            screen.blit(text, (int(SCREEN_SIZE[0] / 2 - text.get_width() / 2), 10))
            if kromb.vida > 0 and nave.powerup!='nuke': #Continua gerando palavras ate Kromb morrer 
                sorteio = random.randint(0, len(banco)-1)
                aux = banco[sorteio]
                del (banco[sorteio])
                fase.ordem = cria_palavras(aux.ordem)
                fase.frase = aux.frase
                fase.resetFase()
                usou = False
        elif fase.estado=='errou':
            t = pygame.time.get_ticks()
            temponovo = t
            fase.estado='reiniciando'
        elif fase.estado == 'reiniciando':
            temponovo+=9
            if t+1000 < temponovo:
                 fase.resetFase()

        #Movimentação dos asteroides
        for i in range (0,len(asteroides),1):
            asteroides[i].y+=1
            if(asteroides[i].y >600):
                asteroides[i].colisao = True
                asteroides[i].sprite = pygame.image.load(explosion_sprite).convert_alpha()


        #Movimentação do Kromb
        increm = kromb.move()
                
        #Movimentar balas ate sairem da cena
        for i in range(0, len(bullets) , 1):
            if i<len(bullets):
                if not bullets[i].colisao:
                    bullets[i].move()
                    if(bullets[i].y < 0):
                        bullets.remove(bullets[i])
                    else:
                        screen.blit(bullets[i].sprite, (bullets[i].x-10,bullets[i].y-20))
                        #pygame.draw.rect(screen, (255, 0, 0), (bullets[i].retangulo.x , bullets[i].retangulo.y,bullets[i].retangulo.w,bullets[i].retangulo.h), 1)
                else:
                    bullets.remove(bullets[i])
        #Impedir nave de sair da tela


        #atualiza a janela
        pygame.display.update()
        fpsClock.tick(FPS)


    return estado_jogo, nave.pontos,fase.tempo

#Loop Game
while True:
    nave_sprite=""
    niveis_completados = 0
    scoreTotal = 0
    scoreFase = 0
    tempoTotal = 0
    TempoFase = 0
    estado_jogo = "jogando"
    backgrounds_jogo = ['Images/background/background_1.png','Images/background/background_2.png' ,'Images/background/background_3.png', 'Images/background/background_4.png' ]

    #pygame.mixer.music.load('Audio/main_menu.wav')
    pygame.mixer.music.load('Audio/level_theme2.wav')
    pygame.mixer.music.set_volume(0.06)
    pygame.mixer.music.play(loops=-1) 

    if(musica == False):
        pygame.mixer.music.pause()
    
    menu_selecao, musica, efeitos_sonoros = menu(musica,efeitos_sonoros)
    
        
    if(menu_selecao == -1): #Sair
        #sys.exit()
        pygame.quit()
        
    elif(menu_selecao == 1): #Jogar
        pular_historia = pularHistoria()
        if (pular_historia > 0): #Assistir Introdução
            if (musica == True):
                pygame.mixer.music.load('Audio/inicio.wav')
                pygame.mixer.music.set_volume(0.15)
                pygame.mixer.music.play(loops=-1)
            historia("intro")
        if(pular_historia >= -1): #Pular Introdução
            if(musica == True):
                pygame.mixer.music.load('Audio/level_theme.mp3')
                #pygame.mixer.music.load('Audio/level_theme2.wav')
                pygame.mixer.music.set_volume(0.03)
                pygame.mixer.music.play(loops=-1)  
            nave_sprite, voltar = escolher_cor_nave()
            if(voltar == False):   
                while(estado_jogo != "game over" and niveis_completados <3):

                    #Seleciona Background para niveis 
                    index = random.randint(0,len(backgrounds_jogo) -1)
                    background_nivel = backgrounds_jogo[index]
                    backgrounds_jogo.remove(background_nivel)

                    #Nivel inicia
                    estado_jogo,scoreFase,tempoFase = nivel(nave_sprite,niveis_completados+1,background_nivel)
                    tempoFase = int(tempoFase)
                
                    if(estado_jogo != "game over"): #Nivel Completo
                        niveis_completados+=1
                        scoreFase = telaNivelCompleto(scoreFase,tempoFase)
                        scoreTotal += scoreFase 
                        tempoTotal += tempoFase
                    else:   #GameOver
                        pygame.mixer.music.pause() #Pausa a Musica
                        scoreTotal += scoreFase 
                        tempoTotal += tempoFase
                        telaGameOver(scoreTotal,tempoTotal,niveis_completados)
                        
                if(niveis_completados == 3): #Nivel Final
                    if (musica == True):
                        pygame.mixer.music.load('Audio/meio.wav')
                        pygame.mixer.music.set_volume(0.15)
                        pygame.mixer.music.play(loops=-1)
                    historia("boss")
                    
                    estado_jogo,scoreFase,tempoFase = Boss(nave_sprite)
                    tempoFase = int(tempoFase)
                    scoreTotal += scoreFase
                    tempoTotal += tempoFase
                    pygame.mixer.music.pause()
                    if(estado_jogo == "game over"):   #GameOver
                        pygame.mixer.music.pause() #Pausa a Musica
                        telaGameOver(scoreTotal,tempoTotal,niveis_completados)
                    else:
                        if (musica == True):
                            pygame.mixer.music.load('Audio/final.wav')
                            pygame.mixer.music.set_volume(0.15)
                            pygame.mixer.music.play(loops=-1)
                        historia("fim")
                        scoreTotal*=2

                teste = verScore(username,scoreTotal)
                rankingPontos(teste, scoreTotal)

    elif(menu_selecao == 2): #Instrucoes e Dicas
        instrucoes_controles()
        instrucoes_jogo()
        instrucoes_interface()
        instrucoes_powerups()
    else:
        creditos()
        
    pygame.display.update()

