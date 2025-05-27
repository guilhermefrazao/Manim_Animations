from tkinter import Grid
import manim
import scipy.signal
import itertools as it

from PIL import Image
from manim import *


class ImageConvolution(Scene):
    image_name = "images/Lula_imposto"
    image_height = 6.0
    kernel_tex = None
    scalar_conv = False
    pixel_stroke_width = 1.0
    pixel_stroke_opacity = 1.0
    kernel_decimal_places = 2
    kernel_color = BLUE
    grayscale = False

    def setup(self):
        super().setup()
        pixels = self.get_pixel_value_array() / 255.0
        kernel = self.get_kernel()
        if self.scalar_conv:
            conv = scipy.signal.convolve(pixels.mean(2), kernel, mode='same')
        else:
            conv = scipy.signal.convolve(pixels, np.expand_dims(kernel, 2), mode='same')

        conv = np.clip(conv, -1, 1)

        pixel_array = self.get_pixel_array(pixels)
        kernel_array = self.get_kernel_array(kernel, pixel_array, tex=self.kernel_tex)
        conv_array = self.get_pixel_array(conv)

        conv_array.set_fill(opacity=0)

        VGroup(pixel_array, conv_array).arrange(RIGHT, buff=2.0)
        kernel_array.move_to(pixel_array[0])

        self.add(pixel_array)
        self.add(conv_array)
        self.add(kernel_array)

        index_tracker = ValueTracker(0)

        def get_index():
            return int(clip(index_tracker.get_value(), 0, len(pixel_array) -1))
        
        kernel_array.add_updater(lambda m: m.move_to(pixel_array[get_index()]))
        conv_array.add_updater(lambda m: m.set_fill(opacity=0))
        conv_array.add_updater(lambda m: m[:get_index() + 1].set_fill(opacity=1))
                               
        right_rect = conv_array[0].copy()
        right_rect.set_fill(opacity=0)
        right_rect.set_stroke(self.kernel_color,4, opacity=1)
        right_rect.add_updater(lambda m: m.move_to(conv_array[get_index()]))
        self.add(right_rect)

        self.index_tracker = index_tracker
        self.pixel_array = pixel_array
        self.kernel_array = kernel_array
        self.conv_array = conv_array
        self.right_rect = right_rect

    def get_pixel_value_array(self):
        im_path = get_full_raster_image_path(self.image_name)
        image = Image.open(im_path)
        return np.array(image)[:, :, :3]
    
    def get_pixel_array(self, array: np.ndarray):
        height, width = array.shape[:2]

        pixel_array = Square().arrange_in_grid(rows=height, cols=width, buff=0.5)
        for pixel, value in zip(pixel_array, it.chain(*array)):
            if value.size == 3:
                rgb = np.abs(value).clip(0,1)
                if self.grayscale:
                    rgb[:] = rgb.mean
            else:
                rgb = [max(-value, 0), max(value, 0), max(value, 0)]
            pixel.set_fill(rgb_to_color(rgb), 1.0)
        pixel_array.set_height(self.image_height)
        pixel_array.set_max_width(5.75)
        pixel_array.set_stroke(WHITE, self.pixel_stroke_width, self.pixel_stroke_opacity)

        return pixel_array
    
    def get_kernel_array(self, kernel: np.ndarray, pixel_array: VGroup, tex=None):
        kernel_array = VGroup()
        values = VGroup()
        for row in kernel:
            for x in row:
                square = pixel_array[0].copy()
                square.set_fill(BLACK, 0)
                square.set_stroke(self.kernel_color, 2, opacity=1)
                if tex:
                    value = Tex(tex)
                else:
                    value = DecimalNumber(x, num_decimal_places=self.kernel_decimal_places)
                value.set_width(square.get_width() * 0.7)
                value.move_to(square)
                value.set_stroke(BLACK, width=3, background=True)
                values.add(value)
                square.add(value)
                kernel_array.add(square)
        for value in values:
            value.set_height(values[0].get_height())
        kernel_array.submobjects.reverse()
        kernel_array.arrange_in_grid(*kernel.shape, buff=0)
        kernel_array.move_to(pixel_array[0])
        return kernel_array

    def get_kernel(self):
        return np.ones((3, 3)) / 9

    def set_index(self, value, run_time=8, rate_func=linear):
        self.play(
            self.index_tracker.animate.set_value(value),
            run_time=run_time,
            rate_func=rate_func
        )

    def zoom_to_kernel(self, run_time=2):
        ka = self.kernel_array
        square = Square().scale(2)
        label = Text("Foco no quadrado").next_to(square, UP)
        self.add(square, label)

        self.play(
            square.animate.scale(0.5).move_to(ORIGIN),
            label.animate.scale(0.5).move_to(ORIGIN + UP)
        )

    def zoom_to_new_pixel(self, run_time=4):
        ka = self.kernel_array
        ca = self.conv_array
        FRAME_HEIGHT = 837
        FRAME_WIDTH = 1184  
        frame = self.camera.frame
        curr_center = frame.get_center().copy()
        index = int(self.index_tracker.get_value())
        new_center = ca[index].get_center()
        center_func = bezier([curr_center, curr_center, new_center, new_center])

        target_height = 1.5 * ka.get_height()
        height_func = bezier([
            frame.get_height(), frame.get_height(), FRAME_HEIGHT,
            target_height, target_height,
        ])
        self.play(
            UpdateFromAlphaFunc(frame, lambda m, a: m.set_height(height_func(a)).move_to(center_func(a))),
            run_time=run_time,
            rate_func=linear,
        )

    def reset_frame(self, run_time=2):
        self.play(
            self.camera.frame.animate.to_default_state(),
            run_time=run_time
        )

    def show_pixel_sum(self, tex=None, convert_to_vect=True, row_len=9):
        # Setup sum
        ka = self.kernel_array
        pa = self.pixel_array
        frame = self.camera.frame
        FRAME_HEIGHT = 837
        FRAME_WIDTH = 1184  

        rgb_vects = VGroup()
        lil_pixels = VGroup()
        expr = VGroup()

        ka_copy = VGroup()
        stroke_width = 2 * FRAME_HEIGHT / frame.get_height()

        lil_height = 1.0
        for square in ka:
            ka_copy.add(square.copy().set_stroke(TEAL, stroke_width))
            sc = square.get_center()
            pixel = pa[np.argmin([np.linalg.norm(p.get_center() - sc) for p in pa])]
            color = pixel.get_fill_color()
            rgb = color_to_rgb(color)
            rgb_vect = DecimalMatrix(rgb.reshape((3, 1)), num_decimal_places=2)
            rgb_vect.set_height(lil_height)
            rgb_vect.set_color(color)
            if np.linalg.norm(rgb) < 0.1:
                rgb_vect.set_color(WHITE)
            rgb_vects.add(rgb_vect)

            lil_pixel = pixel.copy()
            lil_pixel.match_width(rgb_vect)
            lil_pixel.set_stroke(WHITE, stroke_width)
            lil_pixels.add(lil_pixel)

            if tex:
                lil_coef = Tex(tex, font_size=36)
            else:
                lil_coef = square[0].copy()
                lil_coef.set_height(lil_height * 0.5)
            expr.add(lil_coef, lil_pixel, Tex("+", font_size=48))

        expr[-1].scale(0, about_edge=LEFT)  # Stray plus
        rows = VGroup(*(
            expr[n:n + 3 * row_len]
            for n in range(0, len(expr), 3 * row_len)
        ))
        for row in rows:
            row.arrange(RIGHT, buff=0.2)
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        expr.set_max_width(FRAME_WIDTH - 1)
        expr.to_edge(UP)
        expr.fix_in_frame()

        for vect, pixel in zip(rgb_vects, lil_pixels):
            vect.move_to(pixel)
            vect.set_max_width(pixel.get_width())
        rgb_vects.fix_in_frame()

        # Reveal top
        top_bar = FullScreenRectangle().set_fill(BLACK, 1)
        top_bar.set_height(rgb_vects.get_height() + 0.5, stretch=True, about_edge=UP)
        top_bar.fix_in_frame()

        self.play(
            frame.animate.scale(1.2, about_edge=DOWN),
            FadeIn(top_bar, 2 * DOWN),
        )

        # Show sum
        for n in range(len(ka_copy)):
            self.remove(*ka_copy)
            self.add(ka_copy[n])
            self.add(expr[:3 * n + 2])
            self.wait(0.25)
        self.remove(*ka_copy)
        if convert_to_vect:
            self.play(LaggedStart(*(
                Transform(lil_pixel, rgb_vect)
                for lil_pixel, rgb_vect in zip(lil_pixels, rgb_vects)
            )))
        self.wait()
        result = VGroup(top_bar, expr)
        return result
    
class GaussianBluMario(ImageConvolution):
    kernel_decimal_places = 3
    focus_index = 256
    final_run_time = 10

    def construct(self):
        # March!
        self.set_index(self.focus_index)
        self.wait()
        self.zoom_to_kernel()
        self.wait()

        # Gauss surface
        kernel_array = self.kernel_array

        gaussian = ParametricFunction(
            lambda u: (u*2),
            t_range=(0, 1),
            scaling=(101, 101),
        )

        gaussian.set_color(BLUE, 0.8)
        gaussian.match_width(kernel_array)
        gaussian.stretch(2, 2)
        gaussian.add_updater(lambda m: m.move_to(kernel_array, IN))

        self.play(
            FadeIn(gaussian),
            kernel_array.animate.reorient(10, 70),
            run_time=3
        )
        self.wait()
        top_bar = self.show_pixel_sum(convert_to_vect=False)
        self.wait()
        self.zoom_to_new_pixel()
        self.wait()
        self.play(
            kernel_array.animate.set_height(8).reorient(0, 60).move_to(ORIGIN),
            FadeOut(top_bar, time_span=(0, 1)),
            run_time=3,
        )

        # More walking
        self.set_index(len(self.pixel_array), run_time=self.final_run_time)
        self.wait()

    def get_kernel(self):
        # Oh good, hard coded, I hope you feel happy with yourself.
        return np.array([
            [0.00296902, 0.0133062, 0.0219382, 0.0133062, .00296902],
            [0.0133062, 0.0596343, 0.0983203, 0.0596343, 0.0133062],
            [0.0219382, 0.0983203, 0.162103, 0.0983203, 0.0219382],
            [0.0133062, 0.0596343, 0.0983203, 0.0596343, 0.0133062],
            [0.00296902, 0.0133062, 0.0219382, 0.0133062, 0.00296902],
        ])