import pygame
from sys import exit
from pygame.locals import *

n = 0
R = [[], [], [], [], []]

while 2**n < 2**5:
    x = 0
    while x < 2**5:
        if (x // (2**n)) % 2 != 0:
            R[n].append(x)
        x += 1
    n += 1

pygame.init()

largura = 1310
altura = 790
tela = pygame.display.set_mode((largura, altura))

fonte = pygame.font.SysFont(None, 40)
fonte_grande = pygame.font.SysFont(None, 52)

l_carta = 250
a_carta = 400

Cartas = [
    pygame.Rect(10, 100, l_carta, a_carta),
    pygame.Rect(270, 100, l_carta, a_carta),
    pygame.Rect(530, 100, l_carta, a_carta),
    pygame.Rect(790, 100, l_carta, a_carta),
    pygame.Rect(1050, 100, l_carta, a_carta)
]

cartas_selecionadas = [False]*5
cartas_visiveis = [True]*5
offset_y = [0]*5

botao_pensei = pygame.Rect(550, 540, 200, 60)
botao_pronto = pygame.Rect(550, 540, 200, 60)
botao_reiniciar = pygame.Rect(520, 600, 260, 60)

estado = 0
tempo_pausa = 0
resposta = 0

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    tela.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONDOWN:
            mouse = event.pos

            if estado == 0:
                if botao_pensei.collidepoint(mouse):
                    estado = 1

            elif estado == 1:
                for i, carta in enumerate(Cartas):
                    if carta.collidepoint(mouse):
                        cartas_selecionadas[i] = not cartas_selecionadas[i]

                if botao_pronto.collidepoint(mouse):
                    resposta = 0
                    for i in range(5):
                        if cartas_selecionadas[i]:
                            resposta += R[i][0]
                    estado = 2

            elif estado == 4:
                if botao_reiniciar.collidepoint(mouse):
                    cartas_selecionadas = [False]*5
                    cartas_visiveis = [True]*5
                    offset_y = [0]*5
                    estado = 0

    if estado == 0:
        texto = fonte_grande.render("Pense em um número (dia do mês)", True, (0, 0, 0))
        rect_texto = texto.get_rect(center=(largura//2, 40))
        tela.blit(texto, rect_texto)

    if estado == 1:
        texto = fonte_grande.render("Clique nas cartas que contêm o número", True, (0, 0, 0))
        rect_texto = texto.get_rect(center=(largura//2, 40))
        tela.blit(texto, rect_texto)

    if estado == 2:
        for i in range(5):
            if not cartas_selecionadas[i]:
                offset_y[i] += 12
                if offset_y[i] > altura:
                    cartas_visiveis[i] = False
        if all(cartas_visiveis[i] or cartas_selecionadas[i] for i in range(5)):
            estado = 3
            tempo_pausa = pygame.time.get_ticks()

    if estado == 3:
        texto = fonte_grande.render("Estou pensando...", True, (0, 0, 0))
        rect_texto = texto.get_rect(center=(largura//2, 40))
        tela.blit(texto, rect_texto)
        if pygame.time.get_ticks() - tempo_pausa > 1200:
            estado = 4

    if estado == 4:
        texto = fonte_grande.render(f"Você pensou no número {resposta}", True, (0, 120, 0))
        rect_texto = texto.get_rect(center=(largura//2, 40))
        tela.blit(texto, rect_texto)

    for i, carta in enumerate(Cartas):
        if not cartas_visiveis[i]:
            continue

        carta_animada = pygame.Rect(carta.x, carta.y + offset_y[i], carta.width, carta.height)

        cor = (100, 70, 20)
        borda = 6

        if cartas_selecionadas[i]:
            cor = (200, 200, 160)
            borda = 10

        pygame.draw.rect(tela, cor, carta_animada)
        pygame.draw.rect(tela, (0, 0, 0), carta_animada, borda)

        x_texto = carta_animada.x + 15
        y_texto = carta_animada.y + 15

        for num in R[i]:
            t = fonte.render(str(num), True, (0, 0, 0))
            tela.blit(t, (x_texto, y_texto))
            y_texto += 95
            if y_texto > carta_animada.bottom - 20:
                y_texto = carta_animada.y + 30
                x_texto += 60

    if estado == 0:
        pygame.draw.rect(tela, (180, 180, 180), botao_pensei)
        pygame.draw.rect(tela, (0, 0, 0), botao_pensei, 3)
        t = fonte.render("Pensei", True, (0, 0, 0))
        rect_t = t.get_rect(center=botao_pensei.center)
        tela.blit(t, rect_t)

    if estado == 1:
        pygame.draw.rect(tela, (180, 180, 180), botao_pronto)
        pygame.draw.rect(tela, (0, 0, 0), botao_pronto, 3)
        t = fonte.render("Pronto", True, (0, 0, 0))
        rect_t = t.get_rect(center=botao_pronto.center)
        tela.blit(t, rect_t)

    if estado == 4:
        pygame.draw.rect(tela, (180, 180, 180), botao_reiniciar)
        pygame.draw.rect(tela, (0, 0, 0), botao_reiniciar, 3)
        t = fonte.render("Jogar novamente", True, (0, 0, 0))
        rect_t = t.get_rect(center=botao_reiniciar.center)
        tela.blit(t, rect_t)

    pygame.display.update()
