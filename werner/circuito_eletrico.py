import pygame
from pygame.locals import *
from sys import exit
import math

pygame.init()

largura = 900
altura = 600
tela = pygame.display.set_mode((largura, altura))


class Lampada:
    def __init__(self, x, y, raio=20):
        self.x = x
        self.y = y
        self.raio = raio
        self.arrastando = False
        self.slot = None  

    def desenhar(self):
        if self.slot and self.slot.acesa:
            cor = (255, 255, 0)
        else:
            cor = (100, 100, 100)

        pygame.draw.circle(tela, cor, (self.x, self.y), self.raio)

    def mover(self, pos):
        self.x, self.y = pos

    def colide_com_slot(self, slot):
        dx = self.x - slot.x
        dy = self.y - slot.y
        dist = math.hypot(dx, dy)
        return dist < self.raio + slot.raio


class Slot:
    def __init__(self, x, y, raio=25):
        self.x = x
        self.y = y
        self.raio = raio
        self.ocupado = None
        self.acesa = False

    def desenhar(self):
        if self.acesa:
            cor = (0, 255, 0)
        else:
            cor = (200, 0, 0)

        pygame.draw.circle(tela, cor, (self.x, self.y), self.raio)


class Botao:
    def __init__(self, x=20, y=20, L=100, A=40):
        self.x = x
        self.y = y
        self.L = L
        self.A = A
        self.pressionado = False

    def desenhar(self):
        if self.pressionado:
            cor = (150, 150, 150)
        else:
            cor = (220, 220, 220)

        pygame.draw.rect(tela, cor, (self.x, self.y, self.L, self.A))
        pygame.draw.rect(tela, (0, 0, 0), (self.x, self.y, self.L, self.A), 2)

   
    def foi_clicado(self, pos):
        mouse_x = pos[0]
        mouse_y = pos[1]

        dentro_do_x = self.x <= mouse_x <= self.x + self.L
        dentro_do_y = self.y <= mouse_y <= self.y + self.A

        return dentro_do_x and dentro_do_y
   


slots_serie = [Slot(200, 250), Slot(450, 250), Slot(700, 250)]

lampadas = [Lampada(150, 100), Lampada(300, 100), Lampada(500, 100)]

botao = Botao()

def atualizar():

    if botao.pressionado:
        alguma_ocupada = False
        for slot in slots_serie:
            if slot.ocupado:
                alguma_ocupada = True
                break
        for slot in slots_serie:
            slot.acesa = alguma_ocupada
        return
    
    serie_completo = True

    for slot in slots_serie:
        if not slot.ocupado:
            serie_completo = False
            break

    for slot in slots_serie:
        slot.acesa = serie_completo


arrastando = None

f_1 = pygame.Rect(largura//2 - 350, altura - 75, 300, 5)
f_2 = pygame.Rect(largura//2 +50 , altura - 75, 300, 5)

f_s1 = pygame.Rect(largura//2 - 350, altura-350 , 5, 280)
f_s2 = pygame.Rect(largura//2 - 350, altura-350 , 700, 5)
f_s3 = pygame.Rect(largura//2 +350, altura-350 , 5, 280)

f_p1 = pygame.Rect(largura//2 - 350, altura-420 , 5, 350)
f_p2 = pygame.Rect(largura//2 - 350, altura-420 , 700, 5)
f_p3 = pygame.Rect(largura//2 - 350, altura-280 , 700, 5)
f_p4 = pygame.Rect(largura//2 +350, altura-420 , 5, 350)
f_p5 = pygame.Rect(200, altura-420, 5, 140)
f_p6 = pygame.Rect(450, altura-420, 5, 140)
f_p7 = pygame.Rect(700, altura-420, 5, 140)



fios_serie = [f_1, f_2, f_s1, f_s2, f_s3]
fios_paralelo = [f_1, f_2, f_p1, f_p2, f_p3, f_p4, f_p5,f_p6, f_p7]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONDOWN:

            if botao.foi_clicado(event.pos):
                botao.pressionado = not botao.pressionado
                atualizar()

            for lamp in lampadas:
                dx = lamp.x - event.pos[0]
                dy = lamp.y - event.pos[1]
                dist = math.hypot(dx, dy)

                if dist < lamp.raio:
                    lamp.arrastando = True
                    arrastando = lamp

                    if lamp.slot:
                        lamp.slot.ocupado = None
                        lamp.slot = None

                    break

        if event.type == MOUSEBUTTONUP:
            if arrastando:
                encaixou = False

                for slot in slots_serie:
                    if arrastando.colide_com_slot(slot) and not slot.ocupado:

                        arrastando.x = slot.x
                        arrastando.y = slot.y
                        arrastando.slot = slot
                        slot.ocupado = arrastando
                        encaixou = True
                        break

                arrastando.arrastando = False
                arrastando = None
                atualizar()

        if event.type == MOUSEMOTION:
            if arrastando:
                arrastando.mover(event.pos)

    tela.fill((255, 255, 255))

    bateria = pygame.Rect(largura//2-50, altura-100, 100, 50)

    pygame.draw.rect(tela,(0,0,100), bateria)

    
        
        
    
    botao.desenhar()
    
    for f_s in fios_serie:
        if botao.pressionado == False:
            pygame.draw.rect(tela,(0,0,0),f_s)
        
    for f_p in fios_paralelo:
        if botao.pressionado == True:
            pygame.draw.rect(tela,(0,0,0),f_p)

    for s in slots_serie:
        s.desenhar()

    for lamp in lampadas:
        lamp.desenhar()
        
            

    pygame.display.update()
