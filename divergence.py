from mobject import Mobject
from mobject.image_mobject import MobjectFromRegion
from mobject.tex_mobject import TextMobject
from region import region_from_polygon_vertices
from topics.geometry import Arrow, Dot, Circle
from topics.number_line import NumberPlane
from scene import Scene
from animation.simple_animations import ShowCreation
from animation.transform import Transform, ApplyMethod, FadeOut

from helpers import *


class DivergenceFlow(Scene):
    DEFAULT_CONFIG = {
        "arrow_spacing" : 1,
        "dot_spacing" : 0.5,
        "dot_color" : RED,
        "text_color" : WHITE,
        "arrow_color" : GREEN,
    }
    def use_function(self, function):
        # def normalized_func(point):
            # result = function(point)
            # length = np.linalg.norm(result)
            # if length > 0:
            #     result /= length
            #     # result *= self.arrow_spacing/2.
            # return result
        self.function = function

    def get_points(self, spacing):
        x_radius, y_radius = [
            val-val%spacing
            for val in SPACE_WIDTH, SPACE_HEIGHT
        ]
        return map(np.array, it.product(
            np.arange(-x_radius, x_radius+spacing, spacing),
            np.arange(-y_radius, y_radius+spacing, spacing),
            [0]
        ))


    def add_plane(self):
        self.add(NumberPlane().fade())

    def add_dots(self):
        points = self.get_points(self.dot_spacing)
        self.dots = Mobject(*map(Dot, points))
        self.dots.highlight(self.dot_color)
        self.play(ShowCreation(self.dots))
        self.dither()

    def add_arrows(self):
        if not hasattr(self, "function"):
            raise Exception("Must run use_function first")
        points = self.get_points(self.arrow_spacing)
        points = filter(
            lambda p : np.linalg.norm(self.function(p)) > 0.01,
            points
        )
        angles = map(angle_of_vector, map(self.function, points))
        prototype = Arrow(
            ORIGIN, RIGHT*self.arrow_spacing/2.,
            color = self.arrow_color, 
            tip_length = 0.1,
            buff = 0
        )
        self.arrows = Mobject(*[
            prototype.copy().rotate(angle).shift(point)
            for point, angle in zip(points, angles)
        ])

        self.play(ShowCreation(self.arrows))
        self.dither()


    def flow(self):
        if not hasattr(self, "function"):
            raise Exception("Must run use_function first")
        points = self.get_points(self.dot_spacing)
        end_dots = Mobject(*[
            Dot(point+self.function(point))
            for point in points
        ])
        end_dots.highlight(self.dot_color)

        self.play(Transform(self.dots, end_dots))
        self.dither()

    def label(self, text, time = 5):
        mob = TextMobject(text)
        mob.scale(1.5)
        mob.to_edge(UP)
        rectangle = region_from_polygon_vertices(*[
            mob.get_corner(vect) + 0.3*vect
            for vect in [
                UP+RIGHT,
                UP+LEFT,
                DOWN+LEFT,
                DOWN+RIGHT
            ]
        ])
        mob.highlight(self.text_color)
        rectangle = MobjectFromRegion(rectangle, "#111111")
        rectangle.point_thickness = 3
        self.add(rectangle, mob)
        self.dither(time)
        self.remove(mob, rectangle)



class InwardFlow(DivergenceFlow):
    def construct(self):
        circle = Circle(color = YELLOW_C)
        self.use_function(
            lambda p : -p/(2*np.linalg.norm(0.5*p)**0.5+0.01)
        )
        self.add_plane()
        self.add_arrows()  
        self.play(ShowCreation(circle))
        self.label("""
            Notice that arrows point inward around the origin
        """)
        self.label("""
            Watch what that means as we let particles in \\\\
            space flow along the arrows
        """)
        self.remove(circle)
        circle.scale(0.5)
        self.add_dots()        
        self.flow()
        self.remove(self.arrows)
        self.play(ShowCreation(circle))
        self.label("""
            The density of points around \\\\
            the origin has become greater
        """)

        self.label("""
            This means the divergence of the vector field \\\\
            is negative at the origin:
            $\\nabla \\cdot \\vec{\\textbf{v}}(0, 0) < 0$
        """)
        self.dither()


class OutwardFlow(DivergenceFlow):
    def construct(self):
        circle = Circle(color = YELLOW_C, radius = 2)
        self.use_function(
            lambda p : p/(2*np.linalg.norm(0.5*p)**0.5+0.01)
        )
        self.add_plane()
        self.add_arrows()  
        self.play(ShowCreation(circle))
        self.label("""
            On the other hand, when arrows \\\\
            indicate an outward flow\\dots 
        """)
        self.remove(circle)
        circle.scale(0.5)
        self.add_dots()        
        self.flow()
        self.remove(self.arrows)
        self.play(ShowCreation(circle))
        self.label("""
            The density of points near \\\\
            the origin becomes smaller
        """)
        self.label("""
            This means the divergence of the vector field \\\\
            is positive at the origin:
            $\\nabla \\cdot \\vec{\\textbf{v}}(0, 0) > 0$
        """)
        self.dither()

class ArticleExample(DivergenceFlow):
    def construct(self):
        def raw_function((x, y, z)):
            return (2*x-y, x*x, 0)
        def normalized_function(p):
            result = raw_function(p)
            return result/(np.linalg.norm(result)+0.01)
        self.use_function(normalized_function)

        self.add_plane()
        self.add_arrows()
        self.add_dots()
        self.flow()
        self.remove(self.arrows)
        self.dither()


