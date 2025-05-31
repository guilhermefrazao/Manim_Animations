from manim import *
import numpy as np
from scipy.signal import convolve2d
from PIL import Image

def grayscale_to_color(value):
    return rgb_to_color([value, value, value])

class ConvolucaoAnimada(Scene):
    def construct(self):
        # Carrega e redimensiona a imagem
        imagem = Image.open("images/Lula_imposto.jpeg").convert("L")
        imagem = imagem.resize((20, 20), Image.NEAREST)
        img_array = np.array(imagem) / 255.0

        kernel = np.ones((3, 3)) / 9  # Kernel de media

        # Cria o grid original
        grid_original = self.criar_grid(img_array, left_shift=True)
        self.play(Create(grid_original))

        # Aplica a convolução
        resultado = convolve2d(img_array, kernel, mode='same', boundary='fill', fillvalue=0)

        # Cria o grid do resultado
        grid_resultado = self.criar_grid(resultado, left_shift=False)
        self.play(Create(grid_resultado))

        # Anima o kernel passando por cima da imagem
        kernel_rects = self.criar_kernel_overlay(kernel.shape)
        self.add(*kernel_rects)

        for i in range(1, img_array.shape[0]-1):
            for j in range(1, img_array.shape[1]-1):
                self.mover_kernel(kernel_rects, i, j, grid_original)
                self.wait(0.05)

        self.wait(2)

    def criar_grid(self, matriz, left_shift=True):
        n_rows, n_cols = matriz.shape
        squares = VGroup()

        for i in range(n_rows):
            for j in range(n_cols):
                valor = matriz[i, j]
                cor = grayscale_to_color(valor)
                quadrado = Square(side_length=0.3)
                quadrado.set_fill(cor, opacity=1.0)
                quadrado.set_stroke(WHITE, width=0.5)
                quadrado.move_to(np.array([j, -i, 0]) * 0.3)
                squares.add(quadrado)

        deslocamento = LEFT * 4 if left_shift else RIGHT * 4
        squares.move_to(ORIGIN + deslocamento)
        return squares

    def criar_kernel_overlay(self, shape):
        rows, cols = shape
        rects = []
        for i in range(rows):
            for j in range(cols):
                r = Square(side_length=0.3)
                r.set_stroke(BLUE, width=1.5)
                r.set_fill(color=BLUE, opacity=0.2)
                rects.append(r)
        return rects

    def mover_kernel(self, rects, i, j, grid):
        for k, rect in enumerate(rects):
            dx = k % 3 - 1
            dy = k // 3 - 1
            index = (i + dy) * 20 + (j + dx)
            if 0 <= index < len(grid):
                rect.move_to(grid[index].get_center())
