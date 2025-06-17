from manim import *
from PIL import Image

class OneShotLearning(MovingCameraScene):
    def construct(self):
        #Introduction
        self.camera.frame.set(width=20)

        size_x = 300
        size_y = 200

        title = Text("One-Shot Learning", font_size=48)
        title.to_edge(UP).shift(UP * 1.2)

        imagem1 = Image.open("images/Lula_imposto.jpeg")
        imagem2 = Image.open("images/Jair_Bolsonaro_2019_Portrait_(3x4_cropped).jpg")
        imagem3 = Image.open("images/marcos_perfil.jpeg")

        imagem4 = Image.open("images/Bolsonaro_Peixo.jpeg")
        imagem5 = Image.open("images/Manuel_Gomes.jpg")
        
        imagem1 = imagem1.resize((size_x,size_y))
        imagem2 = imagem2.resize((size_x,size_y))
        imagem3 = imagem3.resize((size_x,size_y))
        imagem4 = imagem4.resize((size_x,size_y))
        imagem5 = imagem5.resize((size_x,size_y))

        imagem1 = ImageMobject(imagem1).scale(1.5)
        imagem2 = ImageMobject(imagem2).scale(1.5)
        imagem3 = ImageMobject(imagem3).scale(1.5)
        imagem4 = ImageMobject(imagem4).scale(1.5).shift(LEFT * 3)
        imagem5 = ImageMobject(imagem5).scale(1.5).next_to(imagem4, DOWN)

        cnn = Rectangle(width=2, height=3).set_fill(GRAY, opacity=0.3).shift(RIGHT * 1)
        cnn_text = Text("CNN").scale(0.7).move_to(cnn.get_center())

        arrow_1 = Arrow(imagem4.get_right(), cnn_text.get_left())

        cnn_accuracia = MathTex("47\\%\\text{ accuracy}").shift(RIGHT * 5)

        arrow_2 = Arrow(cnn_text.get_right(), cnn_accuracia.get_left())

        oneShotGroup = Group(imagem1, imagem2, imagem3).arrange(DOWN, buff=1).to_edge(LEFT).shift(LEFT * 3)

        self.play(FadeIn(oneShotGroup, title))
        self.wait(2)

        self.play(FadeIn(imagem4, cnn_text, cnn_accuracia))
        self.play(GrowArrow(arrow_1), GrowArrow(arrow_2))
        self.wait(2)

        self.play(FadeIn(imagem5))
        self.wait(3)
        
        self.play(FadeOut(oneShotGroup, imagem4, arrow_1, cnn_text, arrow_2, cnn_accuracia, imagem5 , title))

        #Similarity Function

        title_similarity = Text("Similatiry Function", font_size=48)
        title_similarity.to_edge(UP).shift(UP * 1.2)
        
        img1 = Image.open("images/Bolsonaro_Camisa.jpeg")
        img2 = Image.open("images/Bolsonaro_palestra.jpeg")
        img3 = Image.open("images/lula_Linguinha.jpeg")

        img1 = img1.resize((size_x,size_y))

        img1 = ImageMobject(img1)

        img2 = img2.resize((size_x,size_y))

        img2 = ImageMobject(img2)

        img3 = img3.resize((size_x,size_y))

        img3 = ImageMobject(img3)

        cnn = Rectangle(width=2, height=3).set_fill(GRAY, opacity=0.3)
        cnn_text = Text("CNN").scale(0.7).move_to(cnn.get_center())

        SimilarityGroup = Group(img1, img2, img3).arrange(DOWN, buff=1).to_edge(LEFT).shift(LEFT * 3)

        arrow1 = Arrow(img1.get_right(), cnn.get_left() + UP * 0.5)
        arrow2 = Arrow(img2.get_right(), cnn.get_left() + DOWN * 0.5)
        arrow3 = Arrow(img3.get_right(), cnn.get_left() + DOWN * 1)

        feature1 = Rectangle(height=0.5, width=1.5).set_fill(BLUE, opacity=0.5).shift(RIGHT * 4 + UP)
        feature2 = Rectangle(height=0.5, width=1.5).set_fill(GREEN, opacity=0.5).shift(RIGHT * 4 + DOWN)
        feature3 = Rectangle(height=0.5, width=1.5).set_fill(GREEN, opacity=0.5).shift(RIGHT * 4 + DOWN * 3)

        feat_label1 = Text("f1").scale(0.5).move_to(feature1)
        feat_label2 = Text("f2").scale(0.5).move_to(feature2)
        feat_label3 = Text("f3").scale(0.5).move_to(feature3)

        arrow_feat1 = Arrow(cnn.get_right() + UP * 0.5, feature1.get_left())
        arrow_feat2 = Arrow(cnn.get_right() + DOWN * 0.5, feature2.get_left())
        arrow_feat3 = Arrow(cnn.get_right() + DOWN * 2, feature3.get_left())

        similarity_text = MathTex(r"Similarity = \frac{f_1 \cdot f_2}{\|f_1\| \|f_2\|}")
        similarity_text.scale(0.7).move_to(DOWN * 2)

        result = Text("Pocentagem de match").scale(1).next_to(similarity_text, DOWN)

        self.play(FadeIn(SimilarityGroup, title_similarity))
        self.wait(0.5)

        self.play(FadeIn(cnn, cnn_text))
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), GrowArrow(arrow3))
        self.wait(0.5)

        self.play(GrowArrow(arrow_feat1), GrowArrow(arrow_feat2), GrowArrow(arrow_feat3))
        self.play(FadeIn(feature1, feature2, feature3,  feat_label1, feat_label2, feat_label3))
        self.wait(0.5)

        self.play(Write(similarity_text))
        self.wait(0.5)

        self.play(Write(result))
        self.wait(2)

        #Adicionar essa função de similaridade para uma rede cnn e verificar os resultados, estudar como funciona a similaridade e estudar os outros vídeos