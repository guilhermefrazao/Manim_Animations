import manim
from manim import *

class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(Transform(square,circle))
        self.play(square.animate.set_fill(PINK, opacity=0.5))