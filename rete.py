#!/usr/bin/python3
# rete.py
# -*- coding: utf-8 -*-
#
# The python script in this file makes the various parts of a model astrolabe.
#
# Copyright (C) 2010-2020 Dominic Ford <dcf21-www@dcford.org.uk>
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
Render the rete of the astrolabe.
"""

from math import pi, sin, tan, cos, asin, floor

from bright_stars_process import fetch_bright_star_list
from constants import unit_deg, unit_rev, unit_mm, inclination_ecliptic, centre_scaling, r_1, d_12, line_width_base
from graphics_context import BaseComponent
from numpy import arange
from settings import fetch_command_line_arguments
from text import text
from themes import themes


class Rete(BaseComponent):
    """
    Render the rete of the astrolabe.
    """

    def default_filename(self):
        """
        Return the default filename to use when saving this component.
        """
        return "rete"

    def bounding_box(self, settings):
        """
        Return the bounding box of the canvas area used by this component.

        :param settings:
            A dictionary of settings required by the renderer.
        :return:
         Dictionary with the elements 'x_min', 'x_max', 'y_min' and 'y_max' set
        """

        r_outer = r_1 - d_12 * 2.7

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
        language = settings['language']
        theme = themes[settings['theme']]

        context.set_color(color=theme['lines'])

        context.set_font_size(1.0)

        # Define the radii of all the concentric circles drawn on front of mother

        # Outer radius of the rete
        r_2 = r_1 - d_12 * 3 - unit_mm

        # Radius of the hole through the centre
        r_3 = d_12 * centre_scaling

        # Radius of the line denoting the equator
        r_4 = r_2 * tan((90 - inclination_ecliptic) / 2 * unit_deg)

        # Radius of the line denoting the tropic of Cancer
        r_5 = r_4 * tan((90 - inclination_ecliptic) / 2 * unit_deg)

        # Draw the outer edge of rete
        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_2)
        context.stroke()

        # Draw the central hole
        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_3)
        context.stroke()

        # Draw ecliptic
        y_ecl_centre = (r_2 - r_5) / 2  # Ecliptic circle is centred on midpoint between +r_2 and -r_5
        r_ecl_outer = (r_2 + r_5) / 2  # Outer radius of ecliptic circle... circle touches r_2 and -r_5
        r_ecl_inner = r_ecl_outer * 0.9
        r_ecl_centre = (r_ecl_outer + r_ecl_inner * 2) / 3

        # Draw ecliptic as band with outer and inner edges
        context.begin_path()
        context.circle(centre_x=0, centre_y=(r_2 - r_5) / 2, radius=r_ecl_outer)
        context.circle(centre_x=0, centre_y=(r_2 - r_5) / 2, radius=r_ecl_inner)
        context.stroke(line_width=1, color=theme['lines'])

        # Draw tick marks along the ecliptic at 2-degree intervals

        # The maths used here is described in http://adsabs.harvard.edu/abs/1976JBAA...86..219E

        for theta in arange(0 * unit_deg, 359 * unit_deg, 2 * unit_deg):
            # Sine rule
            alpha = asin(y_ecl_centre * sin(theta) / r_ecl_outer)

            # Angles in triangle add up to 180 degrees
            psi = theta + alpha

            # Decide size of tick -- every 30 degrees divide entire ecliptic band; major tick every 10 degrees;
            # all other ticks are smaller
            t = floor((theta / unit_deg) + 0.01)
            if (t % 30) == 0:
                r_tick_inner = r_ecl_inner
            elif (t % 10) == 0:
                r_tick_inner = (r_ecl_outer + r_ecl_inner) / 2
            else:
                r_tick_inner = (3 * r_ecl_outer + r_ecl_inner) / 4

            # Draw tick mark
            context.begin_path()
            context.move_to(x=r_ecl_outer * sin(psi), y=y_ecl_centre + r_ecl_outer * cos(psi))
            context.line_to(x=r_tick_inner * sin(psi), y=y_ecl_centre + r_tick_inner * cos(psi))
            context.stroke()

        # Write zodiacal constellation names around ecliptic. We make the text smaller in the southern hemisphere,
        # because "Sagittarius" has a lot of letters to fit into a small space!
        if not is_southern:
            text_size = 1
        else:
            text_size = 0.7

        # Write labels for the zodiacal constellations
        for i, item in enumerate(text[language]["zodiacal_constellations"]):
            i += 1
            name = item['name']
            if not is_southern:
                theta = (-90 + 15 - 30 * i) * unit_deg
            else:
                theta = (-90 - 15 + 30 * i) * unit_deg
                name = name[:8]

            # Sine rule
            alpha = asin(y_ecl_centre * sin(theta) / r_ecl_outer)

            # Angles in triangle add up to 180 degrees
            psi = -90 * unit_deg - (theta + alpha)

            context.circular_text(text=name, centre_x=0, centre_y=y_ecl_centre, radius=r_ecl_centre * 1.02,
                                  azimuth=psi / unit_deg, spacing=0.9, size=text_size)

        # Set clipping region so that we don't draw stars over the top of the ecliptic belt
        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_2)
        context.begin_sub_path()
        context.circle(centre_x=0, centre_y=0, radius=r_3)
        context.begin_sub_path()
        context.circle(centre_x=0, centre_y=(r_2 - r_5) / 2, radius=r_ecl_outer)
        context.begin_sub_path()
        context.circle(centre_x=0, centre_y=(r_2 - r_5) / 2, radius=r_ecl_inner)
        context.clip()

        # Draw the equator
        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_4)
        context.stroke()

        # Draw the Tropic of Cancer
        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_5)
        context.stroke()

        # Draw constellation stick figures
        for line in open("raw_data/constellation_stick_figures.dat"):
            line = line.strip()

            # Ignore blank lines and comment lines
            if (len(line) == 0) or (line[0] == '#'):
                continue

            # Split line into words
            [name, ra1, dec1, ra2, dec2] = line.split()

            # In the southern hemisphere, we flip the sky upside down
            if is_southern:
                dec1 = -float(dec1)
                ra1 = -float(ra1)
                dec2 = -float(dec2)
                ra2 = -float(ra2)

            # Convert start and end of line into a radius and an azimuth
            theta_point_1 = (90 - float(dec1)) * unit_deg / 2
            r_point_1 = r_4 * tan(theta_point_1)
            if r_point_1 > r_2:
                continue

            theta_point_2 = (90 - float(dec2)) * unit_deg / 2
            r_point_2 = r_4 * tan(theta_point_2)
            if r_point_2 > r_2:
                continue

            # Draw stick figure line
            context.begin_path()
            context.move_to(x=r_point_1 * cos(float(ra1) * unit_deg), y=-r_point_1 * sin(float(ra1) * unit_deg))
            context.line_to(x=r_point_2 * cos(float(ra2) * unit_deg), y=-r_point_2 * sin(float(ra2) * unit_deg))
            context.stroke(dotted=True, line_width=1, color=theme['stick_figures'])

        # Draw stars from Yale Bright Star Catalogue
        for star_descriptor in fetch_bright_star_list()['stars'].values():
            [ra, dec, mag] = star_descriptor[:3]

            # Discard stars fainter than mag 4
            if mag == "-" or float(mag) > 4.0:
                continue

            # In the southern hemisphere, we flip the sky upside down
            ra = float(ra)
            dec = float(dec)
            if is_southern:
                dec *= -1
                ra *= -1

            theta = (90 - dec) * unit_deg / 2
            r = r_4 * tan(theta)

            # Discard stars which are outside the plotted area
            if r > r_2:
                continue

            # Draw a circle to represent this star
            context.begin_path()
            context.circle(centre_x=r * cos(ra * unit_deg), centre_y=-r * sin(ra * unit_deg),
                           radius=0.18 * unit_mm * (5 - mag))
            context.fill(color=theme['lines'])

        # Draw RA scale around the edge of the rete
        r_tick = r_2 * 0.98
        for ra in arange(0, 23.9, 1):
            theta = ra / 24 * unit_rev
            if is_southern:
                ra = 24 - ra
            context.begin_path()
            context.move_to(x=-r_2 * cos(theta), y=-r_2 * sin(theta))
            context.line_to(x=-r_tick * cos(theta), y=-r_tick * sin(theta))
            context.stroke(dotted=False, line_width=1, color=theme['lines'])

            context.text(text="{:.0f}ʰ".format(ra),
                         x=r_tick * cos(theta), y=-r_tick * sin(theta),
                         h_align=0, v_align=-1, gap=unit_mm, rotation=-pi / 2 - theta)

        # Draw six small tick marks within each hour of RA
        r_tick = r_2 * 0.99
        for ra in arange(0, 23.9, 1. / 6):
            theta = ra / 24 * unit_rev
            context.begin_path()
            context.move_to(x=r_2 * cos(theta), y=r_2 * sin(theta))
            context.line_to(x=r_tick * cos(theta), y=r_tick * sin(theta))
            context.stroke()


# Do it right away if we're run as a script
if __name__ == "__main__":
    # Fetch command line arguments passed to us
    arguments = fetch_command_line_arguments(default_filename=Rete().default_filename())

    # Render the rete
    Rete(settings={
        'latitude': arguments['latitude'],
        'language': 'en'
    }).render_to_file(
        filename=arguments['filename'],
        img_format=arguments['img_format']
    )
