import pygame

from pygame.locals import *
from sys import exit

from random import randint


pygame.init()

#som
pygame.mixer.music.set_volume(0.3)

musica = pygame.mixer.music.load("exploration-chiptune-rpg-adventure-theme-336428.mp3")

pygame.mixer.music.play(-1)

comeu = pygame.mixer.Sound("eat-.wav")

#fps

relogio = pygame.time.Clock()

#dimensões da tela
largura = 720
altura = 720

#variáveis de posição - cobra

x=0
y=0
x_c=20
y_c=20
velo = 10

#--------------------
morreu = False

#posição da maçã
a = largura-50
b = altura-50

######
tela = pygame.display.set_mode((largura, altura))
######

fonte = pygame.font.SysFont("arial", 30, True, True)

pontos = 0

fps = 25

#lista da cobra
l_cobra = []

#função que desenha a cobra
def cresce(l_cobra):
    for XeY in l_cobra:
        pygame.draw.rect(tela, (0,255,0),(XeY[0]+1,XeY[1]+1, 23,23))

#função que reseta tudo ao morrer
def recomeçar():
    global pontos, x_c, y_c, l_cobra, l_cabeça, morreu, x,y
    pontos = 0
    x_c=20
    y_c=20
    l_cobra=[]
    l_cabeça=[]
    
    morreu = False
    x=0
    y=0
    
#loop principal   
while True:
    tela.fill((0,0,0))
    relogio.tick(fps)
    
    mensagem = f"Pontos: {pontos}"
    texto = fonte.render(mensagem, False, (255,255,255))

    #verifica eventos
    for event in pygame.event.get():
        
        if event.type == KEYDOWN:
            
            if event.key == K_a:
                if x == velo:
                    pass
                
                else:
                    x= -velo
                    y=0
                    
            if event.key == K_d:
                if x==-velo:
                    pass
                else:
                    x=velo
                    y=0
                
            if event.key == K_w:
                if y==velo:
                    pass
                else:
                    y=-velo
                    x=0
            if event.key == K_s:
                if y == -velo:
                    pass
                else:
                    y=velo
                    x=0



            if event.key == K_LEFT:
                if x == velo:
                    pass
                else:
                    x= -velo
                    y=0
            if event.key == K_RIGHT:
                if x==-velo:
                    pass
                else:
                    x=velo
                    y=0
                
            if event.key == K_UP:
                if y==velo:
                    pass
                else:
                    y=-velo
                    x=0
            if event.key == K_DOWN:
                if y == -velo:
                    pass
                else:
                    y=velo
                    x=0 

        if event.type == QUIT:
            
            pygame.quit()
            exit()
            
    x_c = x_c + x
    y_c = y_c + y
    
    cobra = pygame.draw.rect(tela, (0,255,0),(x_c,y_c,25,25))
    maça = pygame.draw.rect(tela,(255,0,0),(a,b,25,25))

    l_cabeça = []
    l_cabeça.append(x_c)
    l_cabeça.append(y_c)
    l_cobra.append(l_cabeça)
    
    if l_cobra.count(l_cabeça)>1:
        
        fonte2 = pygame.font.SysFont("arial",50,True,True)
        fonte3 = pygame.font.SysFont("arial",20,True,True)
        
        perdeu = "PERDEU!!!"
        
        pressione="Pressione a tecla ESPAÇO para jogar novamente"
        
        textela1 = fonte2.render(perdeu, False, (0,0,0))
        textela2 = fonte3.render(pressione, True, (0,0,0))
        
        ret1 = textela1.get_rect()
        ret2 = textela2.get_rect()
        
        morreu = True
        while morreu:
            tela.fill((255,255,255))
            menu=pygame.draw.rect(tela,(0,255,0),(largura//9,altura//9,550,550))

            for event in pygame.event.get():
                
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        recomeçar()
                        
                if event.type==QUIT:
                        pygame.quit()
                        exit()
                        
            ret1.center = (largura//2, altura//2)
            ret2.center = (largura//2, altura-300)
            
            tela.blit(textela1,ret1)
            tela.blit(textela2,ret2)
            pygame.display.update()
               

    if len(l_cobra)>pontos:
        del l_cobra[0]
       
    if cobra.colliderect(maça):
        a=randint(0, 700)
        b=randint(0, 650)
        pontos = pontos+1
        comeu.play()

        
    cresce(l_cobra)
        


    tela.blit(texto, (500, 25))

    pygame.display.update()


#cobra
        
    if x_c>=largura:
        x_c=-1
        
    elif x_c<=-25:
        x_c=largura-25
        
    if y_c>=altura:
        y_c=-1
        
    elif y_c<=-25:
        y_c=altura-25

#maçã
        
    if a>=largura:
        a=0
    elif a<=-25:
        a=largura-25
        
    if b>=altura+25:
        b=0
    elif b<=-25:
        b=altura-25
