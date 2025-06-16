from manim import *
from PIL import Image

class OneShotLearning(MovingCameraScene):
    def construct(self):
        self.camera.frame.set(width=20)

        size_x = 300
        size_y = 200

        title = Text("One Shot Learning - Detecção com somente 1 exemplo", font_size=60)
        title.to_edge(UP).shift(UP * 1.2)

        imagem1 = Image.open("images/Lula_imposto.jpeg")
        imagem2 = Image.open("images/Jair_Bolsonaro_2019_Portrait_(3x4_cropped).jpg")
        imagem3 = Image.open("images/marcos_perfil.jpeg")

        imagem4 = Image.open("images/Bolsonaro_Peixo.jpeg")
        
        imagem1 = imagem1.resize((size_x,size_y))
        imagem2 = imagem2.resize((size_x,size_y))
        imagem3 = imagem3.resize((size_x,size_y))
        imagem4 = imagem4.resize((size_x,size_y))

        imagem1 = ImageMobject(imagem1).scale(1.5)
        imagem2 = ImageMobject(imagem2).scale(1.5)
        imagem3 = ImageMobject(imagem3).scale(1.5)
        imagem4 = ImageMobject(imagem4).scale(1.5)

        oneShotGroup = Group(imagem1,imagem2,imagem3).arrange(DOWN, buff=1).to_edge(LEFT).shift(LEFT * 3)

        newImageGroup = Group(imagem4)

        self.play(FadeIn(oneShotGroup, title))
        self.wait(2)
        self.play(FadeOut(oneShotGroup))
