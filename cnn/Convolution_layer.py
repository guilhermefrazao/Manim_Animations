from manim import *
import numpy as np
from scipy.signal import convolve2d
from PIL import Image

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 60
class ConvolucaoAnimada(MovingCameraScene):
    def construct(self):
        self.camera.frame.set(width=20)

        imagem = Image.open("images/Squirtle.jpg").convert("RGB")
        img_array = np.array(imagem) / 255.0

        filter = self.filter_value() 
        stride = 1

        r = img_array[:, :, 0]
        g = img_array[:, :, 1]
        b = img_array[:, :, 2]

        grid_r = self.criar_grid_rgb(r, 'r')
        grid_g = self.criar_grid_rgb(g, 'g')
        grid_b = self.criar_grid_rgb(b, 'b')

        convolution_layers = self.add_text(f"Convolution_Layers ",font_size=64, position=UP, deslocamento=0.2)

        RGB_group = VGroup(grid_r, grid_g, grid_b)
        RGB_group.move_to(ORIGIN)
        self.play(FadeIn(RGB_group))
        self.wait(2)
        self.play(FadeOut(RGB_group), FadeOut(convolution_layers))


        self.add_text(f"Filter Size = {filter.shape} , Stride = {stride}, Padding = 0", font_size= 28, position= UP, deslocamento= 0.1)
        self.add_text(f"Dimensao: {img_array.shape}", font_size= 28, position=DOWN, deslocamento= 0.1)

        grid_original = self.criar_grid(img_array, left_shift=True)
        self.play(Create(grid_original))

        # Aplica a convolução
        resultado = self.convolve_rgb_image(img_array, filter)

        # Cria o grid do resultado
        grid_resultado = self.criar_grid(resultado, left_shift=False)
        self.play(Create(grid_resultado))
        
        # Anima o filter passando por cima da imagem
        filter_rects = self.criar_filter_overlay(filter.shape)
        for rect, label in filter_rects:
            self.add(rect, label)

        filter_conv = self.criar_filter_overlay_conv()
        self.add(filter_conv)

        iteraction_i = img_array.shape[0]-1
        iteraction_j = img_array.shape[1]-1

        #iteraction_i = 7
        #iteraction_j = 7
        
        for i in range(1, iteraction_i):
            for j in range(1, iteraction_j):
                self.mover_filter(filter_rects, i, j, grid_original, stride, img_array.shape)
                self.mover_filter_conv(filter_conv, i, j, grid_resultado, img_array.shape)
                self.wait(0.07)

        self.wait(1)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

        grid_resultado_final = self.criar_grid(resultado, left_shift=True)
        
        bias = self.add_text("Bias", font_size = 40, position=RIGHT, deslocamento=0.1)
        soma = MathTex("+").next_to(grid_resultado_final, RIGHT, buff=0.1)
        par_esq = Tex("(").next_to(grid_resultado_final, LEFT, buff=0.1)
        par_dir = Tex(")").next_to(bias, RIGHT, buff=0.1)
        Relu = Tex("ReLU").next_to(par_esq, LEFT, buff=0.1)

        grupo = VGroup(Relu, par_esq, grid_resultado_final, soma, bias, par_dir)
        grupo.move_to(ORIGIN)

        self.play(FadeIn(grupo))
        self.wait(2)

    def filter_value(self):
        #Cria uma matriz 3, 3 formada por 1 e dividi ela por 9.
        return np.ones((3, 3)) / 9

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
        largura_total = n_cols * 0.3
        deslocamento = LEFT * (largura_total / 2 + 1) if left_shift else RIGHT * (largura_total / 2 + 1)
        squares.shift(deslocamento)
        return squares 

    def criar_filter_overlay(self, shape):
        rows, cols = shape
        rects = []
        for i in range(rows):
            for j in range(cols):
                r = Square(side_length=0.3)
                r.set_stroke(BLUE, width=2.5)
                r.set_fill(color=TEAL, opacity=0.1)
                label = MathTex(r"{1}/{9}", font_size=16, color= WHITE).move_to(r.get_center())
                rects.append((r, label))
        return rects
    
    def criar_filter_overlay_conv(self):
        r = Square(side_length=0.3)
        r.set_stroke(BLUE, width=2.5)
        r.set_fill(color=BLUE, opacity=1.0)
        return r

    def mover_filter(self, rects, i, j, grid, stride, shape=20):
        for k, (rect, label) in enumerate(rects):
            dx = k % 3 - 1
            dy = k // 3 - 1

            x = i * stride + dy
            y = j * stride + dx

            index = x * shape[1] + y
            if 0 <= index < len(grid):
                target_pos = grid[index].get_center()
                rect.move_to(target_pos)
                label.move_to(target_pos)

    def mover_filter_conv(self, rects, i, j, grid, shape=20):
        for k, rect in enumerate(rects):
            dx = k % 3 - 1
            dy = k // 3 - 1
            index = (i + dy) * shape[1] + (j + dx)
            print("index: ", index)
            if 0 <= index < len(grid):
                target_pos = grid[index].get_center()
                print("target_pos", target_pos)
                rect.move_to(target_pos)

    def add_text(self, conteudo, font_size, position=UP, deslocamento=0.8, left_shift=True):
        text = MathTex(conteudo, font_size=font_size, color=WHITE)
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
    
    def rgb_float_to_hex(self, r, g, b):
    
        r = max(0, min(1, r))
        g = max(0, min(1, g))
        b = max(0, min(1, b))

        return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

    def criar_grid_rgb(self, matriz, canal):
        n_rows, n_cols = matriz.shape
        largura_total = n_cols * 0.6
        squares = VGroup()

        if canal == 'r':
            deslocamento = LEFT * (largura_total / 2 + 1)
        elif canal == 'g':
            deslocamento = ORIGIN
        else:
            deslocamento = RIGHT * (largura_total / 2 + 1)

        for i in range(n_rows):
            for j in range(n_cols):
                valor = matriz[i, j]
                if canal == 'r':
                    cor = self.rgb_float_to_hex(valor, 0 , 0)
                elif canal == 'g':
                    cor = self.rgb_float_to_hex(0, valor, 0)
                else:
                    cor = self.rgb_float_to_hex(0, 0, valor)
                quadrado = Square(side_length=0.3)
                quadrado.set_fill(cor, opacity=1.0)
                quadrado.set_stroke(GREY, width=2.5)  
                quadrado.move_to(np.array([j, -i, 0]) * 0.3)
                squares.add(quadrado)

        squares.move_to(ORIGIN)
        squares.shift(deslocamento)
        return squares

    def convolve_rgb_image(self, image_rgb, kernel):
        convolved = np.zeros_like(image_rgb)
        for c in range(3):
            convolved[:, :, c] = convolve2d(image_rgb[:, :, c], kernel, mode='same', boundary='fill', fillvalue=0)
        return convolved