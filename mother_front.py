#!/usr/bin/python3
# mother_front.py
# -*- coding: utf-8 -*-
#
# The python script in this file makes the various parts of a model astrolabe.
#
# Copyright (C) 2010-2024 Dominic Ford <https://dcford.org.uk/>
#
# This code is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# You should have received a copy of the GNU General Public License along with
# this file; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

# ----------------------------------------------------------------------------

"""
Render the front of the mother of the astrolabe.
"""

from math import pi, sin, cos, acos, floor

from constants import unit_deg, unit_rev, unit_cm, centre_scaling, r_1, d_12, tab_size
from graphics_context import BaseComponent, GraphicsContext
from numpy import arange
from settings import fetch_command_line_arguments
from themes import themes


class MotherFront(BaseComponent):
    """
    Render the front of the mother of the astrolabe.
    """

    def default_filename(self) -> str:
        """
        Return the default filename to use when saving this component.
        """
        return "mother_front"

    def bounding_box(self, settings: dict) -> dict[str, float]:
        """
        Return the bounding box of the canvas area used by this component.

        :param settings:
            A dictionary of settings required by the renderer.
        :return:
         Dictionary with the elements 'x_min', 'x_max', 'y_min' and 'y_max' set
        """

        r_outer: float = r_1 + 0.5 * unit_cm

        return {
            'x_min': -r_outer,
            'x_max': r_outer,
            'y_min': -r_outer - 2 * unit_cm,
            'y_max': r_outer
        }

    def do_rendering(self, settings: dict, context: GraphicsContext) -> None:
        """
        This method is required to actually render this item.

        :param settings:
            A dictionary of settings required by the renderer.
        :param context:
            A GraphicsContext object to use for drawing
        :return:
            None
        """

        is_southern: bool = settings['latitude'] < 0
        theme: dict[str, tuple[float, float, float, float]] = themes[settings['theme']]

        context.set_color(color=theme['lines'])

        # Define the radii of all the concentric circles to be drawn on front of mother

        # Scale of letters around the edge
        r_2: float = r_1 - d_12 * 1.5

        # Protractor scale
        r_3: float = r_2 - d_12

        # Fine divisions
        r_4: float = r_3 - d_12 / 2

        # Central hole
        r_5: float = d_12 * centre_scaling

        # Draw the handle at the top of the astrolabe
        ang: float = 180 * unit_deg - acos(unit_cm / r_1)
        context.begin_path()
        context.arc(centre_x=0, centre_y=-r_1, radius=2 * unit_cm,
                    arc_from=-ang - pi / 2, arc_to=ang - pi / 2)
        context.move_to(x=0, y=-r_3)
        context.line_to(x=0, y=-r_1 - 2 * unit_cm)
        context.stroke()

        # Draw circles 1-5 onto front of mother
        radius: float
        for radius in (r_1, r_2, r_3, r_5):
            context.begin_path()
            context.circle(centre_x=0, centre_y=0, radius=radius)
            context.stroke()

        # Circle 4 has tab cut out
        context.begin_path()
        context.arc(centre_x=0, centre_y=0, radius=r_4,
                    arc_from=tab_size - pi / 2, arc_to=360 * unit_deg - tab_size - pi / 2)
        context.stroke()

        # Between circles 2 and 4, mark 5-degree intervals
        theta: float
        for theta in arange(5 * unit_deg, 359.9 * unit_deg, 5 * unit_deg):
            context.begin_path()
            context.move_to(x=r_2 * sin(theta), y=-r_2 * cos(theta))
            context.line_to(x=r_4 * sin(theta), y=-r_4 * cos(theta))
            context.stroke()

        # Between circles 3 and 4, draw a fine scale of 1-degree intervals
        for theta in arange(tab_size, 360.1 * unit_deg - tab_size, 1 * unit_deg):
            context.begin_path()
            context.move_to(x=r_3 * sin(theta), y=-r_3 * cos(theta))
            context.line_to(x=r_4 * sin(theta), y=-r_4 * cos(theta))
            context.stroke()

        # Between circles 2 and 3, label every 10 degrees
        rt_1: float = (r_2 + r_3) / 2  # Radius at which to place text labels every 10 degrees
        for theta in arange(-180 * unit_deg, 179 * unit_deg, 10 * unit_deg):
            # Work out angle to display around the rim: counts from 0 to 90 four times, not -180 to 180 degrees!
            if theta < -179 * unit_deg:
                theta_disp: float = theta
            elif theta < - 90 * unit_deg:
                theta_disp = theta + 180 * unit_deg
            elif theta < 0 * unit_deg:
                theta_disp = -theta
            elif theta < 90 * unit_deg:
                theta_disp = theta
            else:
                theta_disp = -theta + 180 * unit_deg

            # Display angles around rim as rounded integers
            theta_disp = floor(theta_disp / unit_deg + 0.01)

            context.set_font_size(1.2)

            # Display right-hand zero as a simple one-digit zero
            if theta_disp == 0:
                theta2: float = theta
                context.text(text="0",
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=0, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)

            # Display a cross sign at the left-hand zero
            elif theta_disp == -180:
                theta2 = theta
                context.set_font_size(2.1)
                context.text(text="\u2720",
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=0, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)

            # Display all other angles as two digits, carefully arranged with one digit on either side of the line
            else:
                theta2 = theta - 0.2 * unit_deg
                context.text(text="{:.0f}".format(theta_disp / 10),
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)
                theta2 = theta + 0.2 * unit_deg
                context.text(text="{:.0f}".format(theta_disp % 10),
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=-1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)

        # Between circles 1 and 2, label 24 hours with large letters. A cross marks midnight.
        rt_1: float = r_1 * 0.55 + r_2 * 0.45
        for i, t in enumerate(["\u2720", "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N",
                               "O", "P", "Q", "R", "S", "T", "U", "X", "Y", "Z"]):
            theta = i / 24 * unit_rev

            # Letters are reversed in the southern hemisphere
            if is_southern:
                theta = -theta

            context.set_font_size(2.0 if i > 0 else 2.8)

            context.text(text=t,
                         x=rt_1 * sin(theta), y=-rt_1 * cos(theta),
                         h_align=0, v_align=0, gap=0,
                         rotation=theta)


# Do it right away if we're run as a script
if __name__ == "__main__":
    # Fetch command line arguments passed to us
    arguments = fetch_command_line_arguments(default_filename=MotherFront().default_filename())

    # Render the front of the mother
    MotherFront(settings={
        'latitude': arguments['latitude'],
        'language': 'en'
    }).render_to_file(
        filename=arguments['filename'],
        img_format=arguments['img_format']
    )
