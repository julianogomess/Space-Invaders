#TESTE NIVEL

import math
import pygame
import random
from pygame.locals import *
from sys import exit

pygame.init()
SCREEN_SIZE =(800,600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0 ,32)

#Classe Nave Jogador
class Nave(object):
    def __init__(self,sprite,x,y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.pontos = 0
        self.vidas = 3

    def move(self,sprite,x,y,increm_x,increm_y):
        self.x +=increm_x
        self.y +=increm_y

#Classe dos Tiros
class Bullet(object):
    def __init__(self,sprite,x,y):
        self.sprite = sprite
        self.x = x
        self.y = y

    def move(self):
        self.y -=30

#Classe para obstaculos - modificar para criar sprites em vez de circulos
class Asteroide:
    def __init__(self,sprite,x, y, raio, increm_x,increm_y,colisao=False):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.raio = raio
        self.increm_x = increm_x
        self.increm_y = increm_y
        self.colisao = colisao

    def move(self, x,y, increm_x, increm_y):
        self.x += increm_x
        self.y += increm_y

def create_vidas(x,y,w,h):
    rect = pygame.Rect(x,y,w,h)

    return rect

def colisao(ast1, ast2):
    #Distancia euclidiana de 2 pontos (centros circunferencias)
    distancia =  math.sqrt( ((ast1.x-ast2.x)**2)+((ast1.y-ast2.y)**2) )
    if (ast1.raio + ast2.raio) >= distancia:
        #Muda a cor para vermelho
        explosion_sprite = 'sprites/explosion.png'
        ast1.sprite = pygame.image.load(explosion_sprite).convert_alpha()
        ast2.sprite = pygame.image.load(explosion_sprite).convert_alpha()
        ast1.colisao = True
        ast2.colisao = True
        return True
    else:
        return False

w,h = 30,30
x,y=0,0
#Criando fontes e textos
pontos_font = pygame.font.Font("fonts/SpaceAdventure.ttf", 14) #Fonte para escrever na tela

#Background
background_image_filename = 'Images/fundo2.jpg'
background = pygame.image.load(background_image_filename).convert_alpha()


#Sprites
kevin_image_filename = 'sprites/kevin.png'
kevin = pygame.image.load(kevin_image_filename).convert_alpha()

nave_image_filename = 'sprites/nave-azul.png'
nave_sprite = pygame.image.load(nave_image_filename).convert_alpha()

bullet_image_filename = 'sprites/bullet.png'
sprite_bullet = pygame.image.load(bullet_image_filename).convert_alpha()

#criar objeto Nave

nave = Nave(nave_sprite,400,300)
increm_x = 0
increm_y = 0
vidas = []

#Balas
bullets =[]
#Asteroides/Palavras
asteroides = []
FPS = 60
fpsClock = pygame.time.Clock()
while True:
    x_draw,y_draw = 760,560 #posicao sprite de vidas
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        #Movimentando a nave
        #Evento KeyDown
        if event.type == KEYDOWN:
            if event.key==K_LEFT:
                increm_x+=-15
            if event.key==K_RIGHT:
                increm_x+=15
            if event.key==K_UP:
                increm_y+=-15
            if event.key==K_DOWN:
                increm_y+=15
            if event.key == pygame.K_SPACE:
                bullet1 = Bullet(sprite_bullet,nave.x+5,nave.y)
                bullet2 = Bullet(sprite_bullet,nave.x+60,nave.y)
                bullets.append(bullet1)
                bullets.append(bullet2)
        
        #Evento KeyUp
        if event.type == KEYUP:
            if event.key==K_LEFT or event.key == K_RIGHT:
                increm_x=0
            if event.key==K_UP or event.key == K_DOWN:
                increm_y=0
        
    #Cria os obstaculos a cada frame em quantidades aleatorias
    if(len(asteroides) <10):
        obst_x = random.randint(50,750)
        obst_y = random.randint(50,450)
        obst_tamanho = random.randint(1,4)
        if(obst_tamanho == 1):
             obst_image_filename = 'sprites/borracha.png'
             obst_raio = 15
             obst_i_x = 1
             obst_i_y = 0
        elif(obst_tamanho == 2):
            obst_image_filename = 'sprites/tesoura.png'
            obst_raio = 25
            obst_i_x = -1
            obst_i_y = 0
        elif(obst_tamanho == 3):
            obst_image_filename = 'sprites/cola.png'
            obst_raio = 40
            obst_i_x = 0
            obst_i_y = -1
        else:
            obst_image_filename = 'sprites/caderno.png'
            obst_raio = 60
            obst_i_x = -1
            obst_i_y = -1
            
        obst_sprite= pygame.image.load(obst_image_filename).convert_alpha()
        asteroides.append(Asteroide(obst_sprite,obst_x,obst_y,obst_raio,obst_i_x,obst_i_y))
        
    nave.move(nave, nave.x, nave.y ,increm_x,increm_y)
    screen.fill((255, 255, 255))
    screen.blit(background, (0,0))
    screen.blit(nave.sprite, (nave.x,nave.y))
    
    
    #Desenhar asteroides
    for i in range(0,len(asteroides),1):
        #circulo = pygame.draw.circle(screen, asteroides[i].cor, (asteroides[i].x, asteroides[i].y), asteroides[i].raio, 1)
        screen.blit(asteroides[i].sprite, (asteroides[i].x,asteroides[i].y))

    #Remove todos os asteroides vermelhos (que colidiram na iteração anterior) Explosao
    for asteroide in asteroides:
        if(asteroide.colisao == True):
            asteroides.remove(asteroide)
            nave.pontos+=10
            
    #Desenhar Interface - pontos 
    pontos_text = pontos_font.render("Pontos: "+str(nave.pontos), True, (0,255,0))
    pontosRect = pontos_text.get_rect()  
    pontosRect.center = (700,10)
    screen.blit(pontos_text, pontosRect)
    if(nave.pontos > 5000 and nave.vidas == 3): #so para testar 1 vez
        nave.vidas-=1
    if(nave.pontos > 10000 and nave.vidas == 2): #so para testar 1 vez
        nave.vidas+=1
    
    #Desenhar Interface - vidas 
    for i in range(0,nave.vidas,1):
        vidas.append(create_vidas(x_draw,y_draw,w,h))
        pygame.draw.rect(screen,(255,0,0),vidas[i]) #define retangulo
        x_draw-=40

    
    #Checar colisões para que sejam removidos na proxima iteração
    for i in range(0,len(asteroides),1):
        for j in range(0,len(asteroides),1):
            if(i!=j):
                colisao(asteroides[i],asteroides[j])
                
    #Movimentação dos asteroides   
    for i in range (0,len(asteroides),1):
        asteroides[i].move(asteroides[i].x,asteroides[i].y, asteroides[i].increm_x, asteroides[i].increm_y)

        #Impedir de sair da tela
        if asteroides[i].x + asteroides[i].raio >= 800 or asteroides[i].x - asteroides[i].raio < 0:
            asteroides[i].increm_x *= -1
        if asteroides[i].y + asteroides[i].raio >= 600 or asteroides[i].y - asteroides[i].raio < 0:
            asteroides[i].increm_y *= -1
    
    #Movimentar balas ate sairem da cena
    for i in range(0, len(bullets) , 1):
        bullets[i].move()
        if(bullets[i].y > 600):
            bullets.remove(bullets[i])
        else:
            screen.blit(bullets[i].sprite, (bullets[i].x,bullets[i].y))

    #Impedir nave de sair da tela
    if nave.x + 100 >= 800:
        nave.x = 700
    elif nave.x - 10 < 0:
        nave.x = 10
    elif nave.y + 80 >= 600:
        nave.y = 520
    elif nave.y - 10 < 0:
        nave.y = 10
            
    #atualiza a janela
    pygame.display.update()
    fpsClock.tick(FPS)

