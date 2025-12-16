import pygame
import random
from sys import exit
from pygame.locals import *

pygame.init()

largura = 1200
altura = 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Escolha a Porta")
clock = pygame.time.Clock()

fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 48)

cenario = pygame.image.load("imagens/cenario.png").convert_alpha()
cenario = pygame.transform.scale(cenario, (largura, altura))

apresentador_frames = []
for i in range(9):
    apresentador_frames.append(
        pygame.image.load(f"imagens/apresentador/{i}.png").convert_alpha()
    )

frame_apresentador = 0
tempo_apresentador = 0

apresentador_img = apresentador_frames[0]
x_apresentador = largura - apresentador_img.get_width() - 20
y_apresentador = altura - apresentador_img.get_height() - 50

porta_fechada = pygame.image.load("imagens/portas/fechada.png").convert_alpha()

porta_abrindo = []
for i in range(1, 14):
    porta_abrindo.append(
        pygame.image.load(f"imagens/portas/abrindo_{i}.png").convert_alpha()
    )

premios = {
    "ouro": pygame.image.load("imagens/premios/ouro.png").convert_alpha(),
    "pato": pygame.image.load("imagens/premios/pato.png").convert_alpha(),
    "porco": pygame.image.load("imagens/premios/porco.png").convert_alpha()
}

portas_rect = []
espaco = 80
largura_porta = porta_fechada.get_width()
inicio_x = (largura - (3 * largura_porta + 2 * espaco)) // 2
y_porta = 300

for i in range(3):
    portas_rect.append(
        pygame.Rect(
            inicio_x + i * (largura_porta + espaco),
            y_porta,
            largura_porta,
            porta_fechada.get_height()
        )
    )

def reiniciar():
    premios_lista = ["ouro", "pato", "porco"]
    random.shuffle(premios_lista)
    return {
        "estado": "escolha",
        "premio_porta": {
            0: premios_lista[0],
            1: premios_lista[1],
            2: premios_lista[2]
        },
        "porta_escolhida": None,
        "porta_final": None,
        "porta_aberta": None,
        "frame_porta": 0,
        "tempo_porta": 0
    }

jogo = reiniciar()

falas = {
    "escolha": "Escolha uma porta: 1, 2 ou 3",
    "troca": "Deseja trocar de porta? (S / N)",
    "nova_escolha": "Escolha outra porta",
    "abrindo": "Vamos ver o que tem atrás da porta...",
    "ganhou": "PARABÉNS! Você ganhou as barras de ouro\nque valem mais do que dinheiro!\nENTER para jogar novamente",
    "perdeu": "HAHA! ERRROUUUU! ENTER para tentar de novo"
}

while True:
    dt = clock.tick(60)
    tempo_apresentador += dt
    jogo["tempo_porta"] += dt

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:

            if jogo["estado"] == "escolha":
                if event.key in (K_KP1, K_KP2, K_KP3):
                    jogo["porta_escolhida"] = event.key - K_KP1
                    jogo["estado"] = "troca"

            elif jogo["estado"] == "troca":
                if event.key == K_s:
                    jogo["estado"] = "nova_escolha"
                elif event.key == K_n:
                    jogo["porta_final"] = jogo["porta_escolhida"]
                    jogo["estado"] = "abrindo"
                    jogo["frame_porta"] = 0
                    jogo["tempo_porta"] = 0

            elif jogo["estado"] == "nova_escolha":
                if event.key in (K_KP1, K_KP2, K_KP3):
                    nova = event.key - K_KP1
                    if nova != jogo["porta_escolhida"]:
                        jogo["porta_final"] = nova
                        jogo["estado"] = "abrindo"
                        jogo["frame_porta"] = 0
                        jogo["tempo_porta"] = 0

            elif jogo["estado"] in ("ganhou", "perdeu"):
                if event.key == K_RETURN:
                    jogo = reiniciar()

    tela.blit(cenario, (0, 0))

    if tempo_apresentador > 120:
        frame_apresentador = (frame_apresentador + 1) % len(apresentador_frames)
        tempo_apresentador = 0

    tela.blit(
        apresentador_frames[frame_apresentador],
        (x_apresentador, y_apresentador)
    )

    for i, rect in enumerate(portas_rect):
        if jogo["estado"] in ("ganhou", "perdeu") and i == jogo["porta_aberta"]:
            tela.blit(premios[jogo["premio_porta"][i]], rect.topleft)
        elif jogo["estado"] == "abrindo" and i == jogo["porta_final"]:
            tela.blit(porta_abrindo[jogo["frame_porta"]], rect.topleft)
        else:
            tela.blit(porta_fechada, rect.topleft)

    linhas = falas[jogo["estado"]].split("\n")
    y = 40
    for linha in linhas:
        texto = fonte_grande.render(linha.strip(), True, (255, 255, 255))
        tela.blit(texto, texto.get_rect(center=(largura // 2, y)))
        y += 45

    if jogo["estado"] == "abrindo" and jogo["tempo_porta"] > 90:
        jogo["frame_porta"] += 1
        jogo["tempo_porta"] = 0
        if jogo["frame_porta"] >= len(porta_abrindo):
            jogo["porta_aberta"] = jogo["porta_final"]
            if jogo["premio_porta"][jogo["porta_aberta"]] == "ouro":
                jogo["estado"] = "ganhou"
            else:
                jogo["estado"] = "perdeu"

    pygame.display.update()
