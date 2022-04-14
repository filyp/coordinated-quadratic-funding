from manim import *
import numpy as np


radii = [1, 1, 3, 2]
offsets = [2, 3, 7, 10]


class CoordinatedQuadraticFunding(Scene):
    def construct(self):
        # Creating shapes
        x_range = 15
        y_range = 10
        axis_scale = 0.7
        ax = Axes(
            x_range=[-x_range, 0],
            y_range=[0, y_range],
            x_length=x_range * axis_scale,
            y_length=y_range * axis_scale,
            axis_config={"color": BLUE},
            tips=False,
        )
        
        h = ValueTracker(0)
        
        arcs = []
        arc_closing_lines = []
        lines = []
        sectors = []
        for radius, offset in zip(radii, offsets):
            arcs.append(Arc(
                radius=radius * axis_scale, 
                arc_center=ax.coords_to_point(-offset,0),
                color=BLUE,
            ))
            arc_closing_lines.append(Line(
                start=ax.coords_to_point(-offset,radius),
                end=ax.coords_to_point(-offset,0),
                color=BLUE,
            ))
            lines.append(Line(
                start=ax.coords_to_point(-offset,0),
                end=ax.coords_to_point(0, h.get_value()),
                color=GREEN,
            ))
            
            angle = np.arctan(h.get_value() / offset)
            sector = Sector(
                outer_radius=radius * axis_scale, 
                color=YELLOW_C,
                start_angle=angle,
                angle=-angle,
                arc_center=ax.coords_to_point(-offset, 0),
            )
            sector.offset = offset
            sector.radius = radius
            sectors.append(sector)
        
        for line in lines:
            line.add_updater(
                lambda x: x.put_start_and_end_on( 
                    x.start,
                    ax.coords_to_point(0, h.get_value()),
                )
            )
            
        for sector in sectors:
            sector.add_updater(
                lambda x: x.become(Sector(
                    outer_radius=x.radius * axis_scale, 
                    color=YELLOW_C,
                    start_angle=np.arctan(h.get_value() / x.offset),
                    angle=-np.arctan(h.get_value() / x.offset),
                    arc_center=ax.coords_to_point(-x.offset, 0),
                ))
            )
            
        
        #Showing shapes
        self.play(Create(ax))
        self.play(
            AnimationGroup(*(Create(arc) for arc in arcs), lag_ratio=0.3),
            AnimationGroup(*(Create(arc_cl) for arc_cl in arc_closing_lines), lag_ratio=0.3)
        )
        self.play(*(Create(line) for line in lines))
        # self.play(*(Create(sector) for sector in sectors))
        self.add(*sectors)
        self.play(h.animate.set_value(2))
        
        for _ in range(3):
            squares = []
            h_acc = 0
            transforms = []
            for sector in sectors:
                area = PI * sector.radius ** 2 * (np.arctan(h.get_value() / sector.offset) / TAU)
                side = np.sqrt(area)
                square = Square(
                    side_length=side * axis_scale,
                    fill_color=YELLOW,
                    fill_opacity=1,
                    stroke_opacity=0,
                )
                x, y, _ = ax.coords_to_point(side / 2, h_acc + side / 2)
                square.set_x(x)
                square.set_y(y)
                squares.append(square)
                h_acc += side
                transforms.append(Transform(sector, square))
                
            sector_copies = [sector.copy() for sector in sectors]
            self.add(*sector_copies)
            self.play(AnimationGroup(*transforms, lag_ratio=0.3))    
            self.add(*squares)
            self.remove(*sector_copies)
            
            # for sector in sectors:
            #     sector.suspend_updating()
            # self.play(*(FadeIn(sector) for sector in sectors))
            # for sector in sectors:
            #     sector.resume_updating()
            # self.play(*(Create(sector) for sector in sectors), h.animate.set_value(h_acc))
            self.play(h.animate.set_value(h_acc))
            self.play(AnimationGroup(*(FadeOut(square) for square in squares), lag_ratio=0.1))
        
        
        
        self.wait(4)