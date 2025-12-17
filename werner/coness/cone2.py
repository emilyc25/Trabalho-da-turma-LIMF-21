import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QSlider
)
from PyQt5.QtCore import Qt
import pyqtgraph.opengl as gl


def gerar_malha_cone(k=0.7, z_min=-6, z_max=6, num_z=140, num_theta=140):
    vertices = []
    faces = []

    valores_z = np.linspace(z_min, z_max, num_z)
    angulos = np.linspace(0, 2*np.pi, num_theta, endpoint=False)

   
    for z in valores_z:
        raio = abs(z) * k
        for theta in angulos:
            x = raio * np.cos(theta)
            y = raio * np.sin(theta)
            vertices.append([x, y, z])

    vertices = np.array(vertices)

   
    for i in range(num_z - 1):
        for j in range(num_theta):
            a = i * num_theta + j
            b = i * num_theta + (j + 1) % num_theta
            c = (i + 1) * num_theta + j
            d = (i + 1) * num_theta + (j + 1) % num_theta
            faces.append([a, c, b])
            faces.append([b, c, d])

    return vertices, np.array(faces)



class Janela(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Seções Cônicas — Construção Geométrica")
        self.resize(1300, 820)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

       
        self.visao_3d = gl.GLViewWidget()
        self.visao_3d.setBackgroundColor((30, 30, 30))
        self.visao_3d.opts["distance"] = 22
        self.visao_3d.opts["azimuth"] = 45
        self.visao_3d.opts["elevation"] = 20
        layout.addWidget(self.visao_3d, stretch=8)

        
        self.rotulo_inclinacao = QLabel("Inclinação do plano")
        self.rotulo_altura = QLabel("Altura do plano")

        self.slider_inclinacao = QSlider(Qt.Horizontal)
        self.slider_inclinacao.setRange(0, 89)
        self.slider_inclinacao.setValue(30)

        self.slider_altura = QSlider(Qt.Horizontal)
        self.slider_altura.setRange(-40, 40)
        self.slider_altura.setValue(0)

        estilo_slider = """
        QSlider::groove:horizontal {
            height: 6px;
            background: #cccccc;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            width: 10px;
            background: #0078d7;
            margin: -4px 0;
            border-radius: 5px;
        }
        """
        self.slider_inclinacao.setStyleSheet(estilo_slider)
        self.slider_altura.setStyleSheet(estilo_slider)

        layout.addWidget(self.rotulo_inclinacao)
        layout.addWidget(self.slider_inclinacao)
        layout.addWidget(self.rotulo_altura)
        layout.addWidget(self.slider_altura)

        self.slider_inclinacao.valueChanged.connect(self.atualizar_cena)
        self.slider_altura.valueChanged.connect(self.atualizar_cena)

        self.atualizar_cena()

 
    def atualizar_cena(self):
        self.visao_3d.clear()

        # ---------- Cone ----------
        k = 0.7
        vertices_cone, faces_cone = gerar_malha_cone(k)

        cone = gl.GLMeshItem(
            vertexes=vertices_cone,
            faces=faces_cone,
            color=(0.45, 0.6, 0.9, 0.45),
            smooth=True,
            drawEdges=False
        )
        self.visao_3d.addItem(cone)

        # ---------- Plano ----------
        angulo = np.deg2rad(self.slider_inclinacao.value())
        altura = self.slider_altura.value() / 5

        eixo_x = np.linspace(-9, 9, 40)
        eixo_y = np.linspace(-9, 9, 40)
        X, Y = np.meshgrid(eixo_x, eixo_y)

        
        Z = Y * np.tan(angulo) + altura

        vertices_plano = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()))

        faces_plano = []
        n = len(eixo_x)
        for i in range(n - 1):
            for j in range(n - 1):
                idx = i * n + j
                faces_plano.append([idx, idx + 1, idx + n])
                faces_plano.append([idx + 1, idx + n + 1, idx + n])

        plano = gl.GLMeshItem(
            vertexes=vertices_plano,
            faces=np.array(faces_plano),
            color=(1.0, 0.82, 0.65, 0.55),
            smooth=False
        )
        self.visao_3d.addItem(plano)

        
        valores_y = np.linspace(-8, 8, 9000)
        tangente = np.tan(angulo)

        segmentos = []
        pontos_pos = []
        pontos_neg = []

        for y in valores_y:
            z = y * tangente + altura
            x_quadrado = (k * z)**2 - y**2

            if x_quadrado >= 0:
                x = np.sqrt(x_quadrado)
                pontos_pos.append(( x, y, z))
                pontos_neg.append((-x, y, z))
            else:
                if len(pontos_pos) > 1:
                    segmentos.append(
                        (np.array(pontos_pos), np.array(pontos_neg))
                    )
                pontos_pos = []
                pontos_neg = []

        if len(pontos_pos) > 1:
            segmentos.append(
                (np.array(pontos_pos), np.array(pontos_neg))
            )

        
        for curva_pos, curva_neg in segmentos:
            self.visao_3d.addItem(gl.GLLinePlotItem(
                pos=curva_pos,
                color=(1, 0, 0, 1),
                width=5,
                antialias=True
            ))
            self.visao_3d.addItem(gl.GLLinePlotItem(
                pos=curva_neg,
                color=(1, 0, 0, 1),
                width=5,
                antialias=True
            ))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Janela()
    janela.show()
    sys.exit(app.exec_())
