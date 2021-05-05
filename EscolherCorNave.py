#ESCOLHER COR DA NAVE

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
SCREEN_SIZE =(800,600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0 ,32)

def create_retangulo(x,y,w,h):
    rect = pygame.Rect(x,y,w,h)

    return rect

w,h = 50,50
cores = [(255,0,0),(255,0,255),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(0,0,0),(255,165,0),(0,100,0)]
dialogos = ["Uma cor classica!","Nao muito meu estilo, mas ok","Luigi","Boa escolha operador","Amarelo bacana","Ciano Top","Eu adoro Linkin Park","Laranja muito bom","Um verde para os fortes"]
retangulos = []
cor_nave = (255,0,0)
x,y=0,0
held = False

#Background
background_image_filename = 'Images/fundo2.jpg'
background = pygame.image.load(background_image_filename).convert_alpha()


#Sprites
kevin_image_filename = 'sprites/kevin.png'
kevin = pygame.image.load(kevin_image_filename).convert_alpha()

#Criando fontes e textos
game_font = pygame.font.Font("fonts/SpaceAdventure.ttf", 24) #Fonte para escrever na tela
text = game_font.render('Escolha a cor da nave USS Galactica', True, (0,255,0))

btn_font = pygame.font.Font("fonts/SpaceAdventure.ttf", 14) #Fonte para escrever na tela
btn_text = btn_font.render('Pronto!', True, (0,255,0))

#Ajustando caixas de texto
textRect = text.get_rect()  
textRect.center = (400,30)

btnRect = btn_text.get_rect()  
btnRect.center = (650,365)
botao_cor = (0,0,0)
#Mensagem default sobre a cor da nave
mensagem = dialogos[0]
dialogo_size = 16

#Sprite Nave
nave_image_filename = 'sprites/nave-vermelha.png'
nave_sprite = pygame.image.load(nave_image_filename).convert_alpha()

while True:
    x_draw,y_draw = 100,70
    game_font2 = pygame.font.Font("fonts/SpaceAdventure.ttf", dialogo_size) #Fonte para escrever na tela
    dialogo = game_font2.render(mensagem, True, (0,255,0), (0,0,0))
    dialogoRect = dialogo.get_rect() 
    dialogoRect.center = (360,350)
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
    for i in range(0,9,1):
        retangulos.append(create_retangulo(x_draw,y_draw,w,h))
        pygame.draw.rect(screen,(cores[i]),retangulos[i]) #define retangulo
        x_draw+=70
        if((i+1)%3 == 0): #3 retangulos por linha
            x_draw=100
            y_draw+=70
    pygame.draw.rect(screen, (255,255,255), (400,160,100,100)) #Nave
    screen.blit(nave_sprite , (400,160,100,100))

    #Desenhar objetos de dialogo
    pygame.draw.rect(screen, (0,0,0), (100,300,400,120))
    pygame.draw.rect(screen, (0,255,0), (100,300,120,120),3)
    screen.blit(kevin, (110,310 )) #desenha sprite na posicao
    screen.blit(dialogo, dialogoRect)
    pygame.draw.rect(screen, (0,255,0), (100,300,400,120),3)

    botao_rect = create_retangulo(600,340,100,50)
    pygame.draw.rect(screen, (0,255,0), botao_rect,3)
    pygame.draw.rect(screen, botao_cor, (600,340,100,50))
    screen.blit(btn_text, btnRect)
    
    #Se o mouse estiver sobre a area de um dos retangulos mudar o sprite:
    for i in range(0,9,1):
        if (retangulos[i].collidepoint(pygame.mouse.get_pos()) and held):
            cor_nave = cores[i] #trocar por sprite da nave
            #Sprite Nave
            if(i == 0):
                nave_image_filename = 'sprites/nave-vermelha.png'
            elif(i == 1):
                nave_image_filename = 'sprites/nave-rosa.png'
            elif(i == 2):
                nave_image_filename = 'sprites/nave-verde.png'
            elif(i == 3):
                nave_image_filename = 'sprites/nave-azul-escura.png'
            elif(i == 4):
                nave_image_filename = 'sprites/nave-amarela.png'
            elif(i == 5):
                nave_image_filename = 'sprites/nave-azul.png'
            elif(i == 6):
                nave_image_filename = 'sprites/nave-preta.png'
            elif(i == 7):
                nave_image_filename = 'sprites/nave-laranja.png'
            else:
                nave_image_filename = 'sprites/nave-verde-escura.png'
            
            nave_sprite = pygame.image.load(nave_image_filename).convert_alpha()
            #Alterar Texto
            mensagem = dialogos[i]
            if(i == 1 or i == 8):
                dialogo_size = 12
            #elif(i == 6):
                #Linkin Park
                #pygame.mixer.music.load('Audio/LP.mp3')
                #pygame.mixer.music.play(-1)
            else:
                dialogo_size = 16

    if(botao_rect.collidepoint(pygame.mouse.get_pos()) and held):
        botao_cor = (255,255,255)
        #carregar proxima tela
        
    pygame.display.update()
