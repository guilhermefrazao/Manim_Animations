from manim import *
import numpy as np
from PIL import Image
import itertools

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 60

class PoolingImagem(MovingCameraScene):
    def construct(self):
        self.camera.frame.set(width=20)

        pooling_type = "Mean"

        imagem = Image.open("images/Squirtle.jpg").convert("RGB")
        
        img_array = np.array(imagem) / 255.0

        stride = 2
        filter_size = 2
        padding = 0
        n_cols = img_array.shape[1]  
        resultado = ((img_array.shape[1] + 2 *(padding) - filter_size) / stride) + 1

        Pooling = self.add_text(f"Pooling_Layers (Mean_Pooling)", font_size= 64 , position= UP, deslocamento=0.6)
        Variables = self.add_text(f"Filter Size = {filter_size} , Stride = {stride}, Padding = {padding}", font_size=32, position= UP, deslocamento=0.1,  left_shift=False)
        Dims = self.add_text(f"Dimensao: {img_array.shape}", font_size= 28, position=DOWN, deslocamento= 0.1)
        conta = self.add_text(fr"DimsFilter = \frac{{{img_array.shape[0]} + 2 \cdot {padding} - {filter_size}}}{{{stride}}} + 1 = {resultado}", font_size= 28, position=DOWN, deslocamento= 0.8, left_shift=False)

        pooled = self.aplicar_pooling(img_array, stride, filter_size,  pooling_type=pooling_type)

        Dims_pool = self.add_text(f"Dimensao: {pooled.shape}", font_size= 28, position=DOWN, deslocamento= 0.1, left_shift=False)

        grid_original = self.criar_grid(img_array, left_shift=True)
        grid_pooled = self.criar_grid(pooled, left_shift=False)

        pooling_filter = self.criar_filter_overlay(filter_size, grid_original, n_cols)

        self.play(FadeIn(Pooling, Variables, Dims, Dims_pool, conta))
        self.play(Create(grid_original), Create(grid_pooled))
        self.play(FadeIn(pooling_filter))

        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def aplicar_pooling(self, matriz, stride, pool_size,  pooling_type="max"):
        n_rows, n_cols, dim = matriz.shape
        r = matriz[:, :, 0]
        g = matriz[:, :, 1]
        b = matriz[:, :, 2]
        pooled = []
        for i in range(0, n_rows - pool_size + 1, stride):
            linha = []
            for j in range(0, n_cols - pool_size + 1, stride):
                bloco_red = r[i:i+pool_size, j:j+pool_size]
                bloco_green = g[i:i+pool_size, j:j+pool_size]
                bloco_blue = b[i:i+pool_size, j:j+pool_size]
                if pooling_type == "max":
                    valor_red = np.max(bloco_red)
                    valor_green = np.max(bloco_green)
                    valor_blue = np.max(bloco_blue)
                else:
                    valor_red = np.mean(bloco_red)
                    valor_green = np.mean(bloco_green)
                    valor_blue = np.mean(bloco_blue)
                linha.append([valor_red, valor_green, valor_blue])
            pooled.append(linha)
        return np.array(pooled)

    def criar_grid(self, matriz, left_shift=True):
        n_rows, n_cols, dim = matriz.shape 
        squares = VGroup()

        for i in range(n_rows):
            for j in range(n_cols):
                valor = matriz[i, j]
                cor = self.rgb_float_to_hex(valor[0], valor[1], valor[2])
                quadrado = Square(side_length=0.3)
                quadrado.set_fill(cor, opacity=1.0)
                quadrado.set_stroke(WHITE, width=0.5)
                quadrado.move_to(np.array([j, -i, 0]) * 0.3)
                squares.add(quadrado)

        squares.move_to(ORIGIN)
        largura_total = 20 * 0.3
        deslocamento = LEFT * (largura_total / 2 + 1) if left_shift else RIGHT * (largura_total / 2 + 1)
        squares.shift(deslocamento)
        return squares 
    
    def rgb_float_to_hex(self, r, g, b):
    
        r = max(0, min(1, r))
        g = max(0, min(1, g))
        b = max(0, min(1, b))

        return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

    def add_text(self, conteudo, font_size,  position=UP, deslocamento=0.8, left_shift=True):
        text = MathTex(conteudo, font_size = font_size, color=WHITE)
        text.to_edge(position)
        text.shift(position * deslocamento)

        quantidade_de_deslocamento = 4
        deslocamento_lateral = LEFT * quantidade_de_deslocamento if left_shift else RIGHT * quantidade_de_deslocamento
        text.shift(deslocamento_lateral)

        fundo = Rectangle(
            width= text.width + 0.3,
            height=text.height + 0.2,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0
        ).move_to(text.get_center())

        grupo = VGroup(fundo, text)
        self.add(grupo)
        return grupo
    
    def criar_filter_overlay(self, pool_size, grid_original, n_cols):
        overlay = VGroup()
        idxs = []

        for i in range(pool_size):
            for j in range(pool_size):
                r = Square(side_length=0.3)
                r.set_stroke(PURPLE, width=2.5)
                r.set_fill(color=TEAL, opacity=0.1)
                r.move_to(np.array([j, -i, 0]) * 0.3)
                overlay.add(r)
            idxs.append([n + (i * n_cols) for n in range(0, pool_size)])        

        flat = list(itertools.chain.from_iterable(idxs))
        centros = [grid_original[i].get_center() for i in flat]
        centro_medio = sum(centros) / len(centros)

        overlay.move_to(centro_medio)
        return overlay