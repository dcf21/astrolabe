#!/usr/bin/python3
# mother_front.py
# -*- coding: utf-8 -*-
#
# The python script in this file makes the various parts of a model astrolabe.
#
# Copyright (C) 2010-2018 Dominic Ford <dcf21-www@dcford.org.uk>
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

from math import sin, cos, acos, floor

from constants import unit_deg, unit_rev, unit_cm, centre_scaling, r_1, d_12, tab_size
from graphics_context import BaseComponent
from numpy import arange
from settings import fetch_command_line_arguments


class MotherFront(BaseComponent):
    """
    Render the front of the mother of the astrolabe.
    """

    def default_filename(self):
        """
        Return the default filename to use when saving this component.
        """
        return "mother_front"

    def bounding_box(self):
        """
        Return the bounding box of the canvas area used by this component.

        :return:
         Dictionary with the elements 'x_min', 'x_max', 'y_min' and 'y_max' set
        """

        r_outer = r_1 + 3 * unit_cm

        return {
            'x_min': -r_outer,
            'x_max': r_outer,
            'y_min': -r_outer,
            'y_max': r_outer
        }

    def do_rendering(self, settings, context):
        """
        This method is required to actually render this item.

        :param settings:
            A dictionary of settings required by the renderer.
        :param context:
            A GraphicsContext object to use for drawing
        :return:
            None
        """

        is_southern = settings['latitude'] < 0

        context.set_font_size(1.2)

        # Radii of circles to be drawn on front of mother
        r_2 = r_1 - d_12 * 1.5
        r_3 = r_2 - d_12
        r_4 = r_3 - d_12 / 2
        r_5 = d_12 * centre_scaling

        # Draw the handle at the top of the astrolabe
        ang = 180 * unit_deg - acos(unit_cm / r_1)
        context.arc(centre_x=0, centre_y=r_1, radius=2 * unit_cm, arc_from=-ang, arc_to=ang)
        context.move_to(x=0, y=r_3)
        context.line_to(x=0, y=r_1 + 2 * unit_cm)

        # Draw circles 1-5 onto front of mother
        context.circle(centre_x=0, centre_y=0, radius=r_1)
        context.circle(centre_x=0, centre_y=0, radius=r_2)
        context.circle(centre_x=0, centre_y=0, radius=r_3)

        # Circle four has tab cut out
        context.arc(centre_x=0, centre_y=0, radius=r_4, arc_from=tab_size, arc_to=360 * unit_deg - tab_size)

        context.circle(centre_x=0, centre_y=0, radius=r_5)

        # Between circles 2 and 4, mark 5-degree intervals
        for theta in arange(5 * unit_deg, 359 * unit_deg, 5 * unit_deg):
            context.move_to(x=r_2 * sin(theta), y=r_2 * cos(theta))
            context.line_to(x=r_4 * sin(theta), y=r_4 * cos(theta))

        # Between circles 3 and 4, draw a fine scale of 1-degree intervals
        for theta in arange(tab_size, 360 * unit_deg - tab_size, 1 * unit_deg):
            context.move_to(x=r_3 * sin(theta), y=r_3 * cos(theta))
            context.line_to(x=r_4 * sin(theta), y=r_4 * cos(theta))

        # Between circles 2 and 3, label every 10 degrees
        rt_1 = (r_2 + r_3) / 2
        for theta in arange(-180 * unit_deg, 179 * unit_deg, 10 * unit_deg):
            if theta < -179 * unit_deg:
                theta_disp = theta
            elif theta < - 90 * unit_deg:
                theta_disp = theta + 180 * unit_deg
            elif theta < 0 * unit_deg:
                theta_disp = -theta
            elif theta < 90 * unit_deg:
                theta_disp = theta
            else:
                theta_disp = -theta + 180 * unit_deg
            theta_disp = floor(theta_disp / unit_deg + 0.01)

            if theta_disp == 0:
                theta2 = theta
                context.text(text="0",
                             x=rt_1 * cos(theta2), y=rt_1 * sin(theta2),
                             h_align=0, v_align=0, gap=0, rotation=theta + 90 * unit_deg)
            elif theta_disp == -180:
                theta2 = theta
                context.text(text="\LARGE\kreuz",
                             x=rt_1 * cos(theta2), y=rt_1 * sin(theta2),
                             h_align=0, v_align=0, gap=0, rotation=theta + 90 * unit_deg)
            else:
                theta2 = theta - 0.2 * unit_deg
                context.text(text="%d" % (theta_disp / 10),
                             x=rt_1 * cos(theta2), y=rt_1 * sin(theta2),
                             h_align=1, v_align=0, gap=0, rotation=theta + 90 * unit_deg)
                theta2 = theta + 0.2 * unit_deg
                context.text(text="%d" % (theta_disp % 10),
                             x=rt_1 * cos(theta2), y=rt_1 * sin(theta2),
                             h_align=-1, v_align=0, gap=0, rotation=theta + 90 * unit_deg)

        # Between circles 1 and 2, label 24 hours with large letters. A cross marks midnight.
        rt_1 = (r_1 + r_2) / 2
        context.set_font_size(2.0)
        i = 0
        for t in ["\LARGE\kreuz", "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R",
                  "S", "T", "U", "X", "Y", "Z"]:
            theta = i / 24 * unit_rev
            if is_southern:
                theta = -theta
            context.text(text="%s" % (t), x=rt_1 * sin(theta), y=rt_1 * cos(theta), h_align=0, v_align=0, gap=0,
                         rotation=-theta)
            i = i + 1


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
