from tkinter import *
from PIL import Image, ImageTk, ImageSequence

# Janela principal
janela = Tk()
janela.title("Atividade de imagens ou gifs em loop")

LARGURA = 400
ALTURA = 400
TEMPO_TROCA = 2000  

arquivos = [
    "ufopa.png",
    "vasco.png",
    "Planificação Icosaedro.gif",
    "piramide.jpg",
    "Octaedro.gif",
    "pará.jpg",
    "brasil.png",
    "dado.jpg",
    "bola.png",
    "natal.jpg",
    "anjo.jpg",
    "onca.jpg"
]

nomes = [
    "Logo UFOPA",
    "Vasco",
    "Planificação Icosaedro",
    "Pirâmide",
    "Planificação Octaedro",
    "Bandeira do Pará",
    "Bandeira do Brasil",
    "Dado",
    "Bola",
    "Natal",
    "Anjo",
    "Onça"
]

indice = 0
frames = []
frame_atual = 0
animacao_id = None

label_imagem = Label(janela)
label_imagem.pack(pady=10)

label_nome = Label(janela, font=("Arial", 20))
label_nome.pack(pady=5)

def carregar_midia():
    global frames, frame_atual, animacao_id

    if animacao_id:
        janela.after_cancel(animacao_id)

    frames = []
    frame_atual = 0

    label_nome.config(text=nomes[indice])
    img = Image.open(arquivos[indice])

    # Se for GIF animado
    if getattr(img, "is_animated", False):
        for frame in ImageSequence.Iterator(img):
            frame = frame.resize((LARGURA, ALTURA))
            frames.append(ImageTk.PhotoImage(frame))
        animar_gif()
    else:
        img = img.resize((LARGURA, ALTURA))
        foto = ImageTk.PhotoImage(img)
        frames.append(foto)
        label_imagem.config(image=foto)

def animar_gif():
    global frame_atual, animacao_id
    label_imagem.config(image=frames[frame_atual])
    frame_atual = (frame_atual + 1) % len(frames)
    animacao_id = janela.after(80, animar_gif)

def proxima_midia():
    global indice
    indice = (indice + 1) % len(arquivos)
    carregar_midia()
    janela.after(TEMPO_TROCA, proxima_midia)

carregar_midia()
janela.after(TEMPO_TROCA, proxima_midia)

janela.mainloop()
