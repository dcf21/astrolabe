#!/usr/bin/python3
# rule.py
# -*- coding: utf-8 -*-
#
# The python script in this file makes the various parts of a model astrolabe.
#
# Copyright (C) 2010-2019 Dominic Ford <dcf21-www@dcford.org.uk>
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
Render the rule and the alidade of the astrolabe.
"""

from math import sin, tan

from constants import unit_deg, unit_cm, unit_mm, inclination_ecliptic, centre_scaling, r_1, d_12
from graphics_context import BaseComponent
from settings import fetch_command_line_arguments
from themes import themes


class Rule(BaseComponent):
    """
    Render the rule and the alidade of the astrolabe.
    """

    def default_filename(self):
        """
        Return the default filename to use when saving this component.
        """
        return "rule"

    def bounding_box(self, settings):
        """
        Return the bounding box of the canvas area used by this component.

        :param settings:
            A dictionary of settings required by the renderer.
        :return:
         Dictionary with the elements 'x_min', 'x_max', 'y_min' and 'y_max' set
        """
        return {
            'x_min': -2 * unit_cm,
            'x_max': 4 * unit_cm,
            'y_min': -r_1 * 1.2,
            'y_max': r_1 * 1.2
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
        theme = themes[settings['theme']]

        context.set_color(color=theme['lines'])

        margin = 2 * unit_cm

        r_2 = r_1 - d_12 * 3 - unit_mm  # Outer radius of rete
        r_3 = d_12 * centre_scaling  # Radius of central hole

        r_4 = r_2 * tan((90 - inclination_ecliptic) / 2 * unit_deg)  # Radius of equator
        r_5 = r_4 * tan((90 - inclination_ecliptic) / 2 * unit_deg)  # Radius of tropic of Cancer

        r_6 = 0.8 * unit_cm  # Width of alidade

        r_12 = r_1 - d_12 * 10  # Outer radius of shadow scale

        # Subroutine to draw outlines of rule and the alidade
        def rule_draw(context, xpos, ypos, sight):
            context.begin_path()
            context.circle(centre_x=xpos, centre_y=ypos, radius=r_3)
            context.stroke()

            context.begin_path()
            context.arc(centre_x=xpos, centre_y=ypos, radius=r_6, arc_from=-90 * unit_deg, arc_to=0)
            context.stroke()

            context.begin_path()
            context.arc(centre_x=xpos, centre_y=ypos, radius=r_6, arc_from=90 * unit_deg, arc_to=180 * unit_deg)
            context.stroke()

            context.begin_path()

            context.move_to(x=xpos, y=ypos + r_6)
            context.line_to(x=xpos, y=ypos + (r_2 + margin) + r_6)
            context.line_to(x=xpos + r_6, y=ypos + (r_2 + margin))
            context.line_to(x=xpos + r_6, y=ypos)

            context.move_to(x=xpos, y=ypos - r_6)
            context.line_to(x=xpos, y=ypos - (r_2 + margin) - r_6)
            context.line_to(x=xpos - r_6, y=ypos - (r_2 + margin))
            context.line_to(x=xpos - r_6, y=ypos)

            context.stroke()

            if sight:
                context.begin_path()
                context.rectangle(x0=xpos, y0=ypos - r_2 * 0.65, x1=xpos + r_2 * 0.1, y1=ypos - r_2 * 0.85)
                context.begin_sub_path()
                context.rectangle(x0=xpos, y0=ypos + r_2 * 0.65, x1=xpos - r_2 * 0.1, y1=ypos + r_2 * 0.85)
                context.stroke()

        # Draw outlines of rule and the alidade
        separation = 2.2 * unit_cm

        context.set_font_size(0.9)

        # Only alidade has a sight
        rule_draw(context, 0 * unit_cm, 0 * unit_cm, False)
        context.text(text="(a) Rule", x=-7 * unit_mm, y=r_2 + margin + 1.5 * r_6)

        rule_draw(context, separation, 0 * unit_cm, True)
        context.text(text="(b) Alidade", x=separation - 7 * unit_mm, y=r_2 + margin + 1.5 * r_6)

        # Draw declination scale on rule
        major_tick_length = 4 * unit_mm
        minor_tick_length = 2 * unit_mm
        if not is_southern:
            context.set_font_size(1.0)
        else:
            context.set_font_size(0.7)

        for dec in range(-25, 71, 5):
            theta = (90 - dec) * unit_deg / 2
            r = r_4 * tan(theta)
            if is_southern:
                dec *= -1
            if (dec < 60) and (dec % 10 == 0):
                context.begin_path()
                context.move_to(x=0, y=-r)
                context.line_to(x=-major_tick_length, y=-r)
                context.stroke()
                context.text(text="{}\u00b0".format(dec), x=-major_tick_length, y=-r,
                             v_align=1, rotation=90 * unit_deg)

                context.begin_path()
                context.move_to(x=0, y=r)
                context.line_to(x=major_tick_length, y=r)
                context.stroke()
                context.text(text="{}\u00b0".format(dec), x=major_tick_length, y=r,
                             v_align=1, rotation=-90 * unit_deg)
            else:
                context.begin_path()
                context.move_to(x=0, y=-r)
                context.line_to(x=-minor_tick_length, y=-r)
                context.move_to(x=0, y=r)
                context.line_to(x=minor_tick_length, y=r)
                context.stroke()

        # Draw solar-altitude scale on alidade
        context.set_font_size(1.0)

        for i in range(20, 91, 5):
            r = r_12 * sin(i * unit_deg)
            context.begin_path()
            context.move_to(x=separation, y=-r)
            context.line_to(x=separation - major_tick_length / 2, y=-r)
            context.move_to(x=separation, y=r)
            context.line_to(x=separation + major_tick_length / 2, y=r)
            context.stroke()

        for i in [20, 35, 50, 80]:
            r = r_12 * sin(i * unit_deg)

            context.begin_path()
            context.move_to(x=separation, y=-r)
            context.line_to(x=separation - major_tick_length, y=-r)
            context.stroke()
            context.text(text="{}\u00b0".format(i), x=separation - major_tick_length, y=-r,
                         v_align=1, rotation=90 * unit_deg)

            context.begin_path()
            context.move_to(x=separation, y=r)
            context.line_to(x=separation + major_tick_length, y=r)
            context.stroke()
            context.text(text="{}\u00b0".format(i), x=separation + major_tick_length, y=r,
                         v_align=1, rotation=-90 * unit_deg)


# Do it right away if we're run as a script
if __name__ == "__main__":
    # Fetch command line arguments passed to us
    arguments = fetch_command_line_arguments(default_filename=Rule().default_filename())

    # Render the rule and alidade
    Rule(settings={
        'latitude': arguments['latitude'],
        'language': 'en'
    }).render_to_file(
        filename=arguments['filename'],
        img_format=arguments['img_format']
    )
