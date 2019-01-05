#!/usr/bin/python3
# mother_back.py
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
Render the back of the mother of the astrolabe.
"""

from math import pi, sin, tan, cos, acos, atan, atan2, floor

from constants import unit_deg, unit_rev, unit_cm, unit_mm, centre_scaling, r_1, d_12
from graphics_context import BaseComponent
from numpy import arange
from settings import fetch_command_line_arguments
from text import text
import calendar
import scipy.interpolate


class MotherBack(BaseComponent):
    """
    Render the back of the mother of the astrolabe.
    """

    def default_filename(self):
        """
        Return the default filename to use when saving this component.
        """
        return "mother_back"

    def bounding_box(self, settings):
        """
        Return the bounding box of the canvas area used by this component.

        :param settings:
            A dictionary of settings required by the renderer.
        :return:
            Dictionary with the elements 'x_min', 'x_max', 'y_min' and 'y_max' set
        """

        r_outer = r_1 + 0.4 * unit_cm

        return {
            'x_min': -r_outer,
            'x_max': r_outer,
            'y_min': -r_outer - 2 * unit_cm,
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

        language = settings['language']

        # Radii of circles to be drawn on back of mother
        r_2 = r_1 - d_12
        r_3 = r_2 - d_12 / 2
        r_4 = r_3 - d_12
        r_5 = r_4 - d_12
        r_6 = r_5 - d_12
        r_7 = r_6 - d_12
        r_8 = r_7 - d_12 / 2
        r_9 = r_8 - d_12
        r_10 = r_9 - d_12
        r_11 = r_10 - d_12
        r_12 = r_11 - d_12
        r_13 = d_12 * centre_scaling

        # Draw the handle at the top of the astrolabe
        ang = 180 * unit_deg - acos(unit_cm / r_1)
        context.begin_path()
        context.arc(centre_x=0, centre_y=-r_1, radius=2 * unit_cm,
                    arc_from=-ang - pi / 2, arc_to=ang - pi / 2)
        context.move_to(x=0, y=-r_1 - 2 * unit_cm)
        context.line_to(x=0, y=-r_1 + 2 * unit_cm)
        context.stroke()

        # Draw circles 1-13 onto back of mother
        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_1)
        context.begin_sub_path()
        context.circle(centre_x=0, centre_y=0, radius=r_13)
        context.stroke(line_width=1)
        context.clip()

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_2)
        context.stroke(line_width=1)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_3)
        context.stroke(line_width=3)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_4)
        context.stroke(line_width=1)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_5)
        context.stroke(line_width=3)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_6)
        context.stroke(line_width=1)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_7)
        context.stroke(line_width=1)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_8)
        context.stroke(line_width=1)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_9)
        context.stroke(line_width=1)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_10)
        context.stroke(line_width=3)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_11)
        context.stroke(line_width=1)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_12)
        context.stroke(line_width=1)

        context.begin_path()
        context.circle(centre_x=0, centre_y=0, radius=r_13)
        context.stroke(line_width=1)

        # Label space between circles 1-5 with passage of Sun through zodiacal constellations

        # Mark every 30 degrees, where Sun enters new zodiacal constellation
        for theta in arange(0 * unit_deg, 359 * unit_deg, 30 * unit_deg):
            context.begin_path()
            context.move_to(x=r_1 * cos(theta), y=-r_1 * sin(theta))
            context.line_to(x=r_5 * cos(theta), y=-r_5 * sin(theta))
            context.stroke()

        # Mark five degree intervals within each zodiacal constellation
        for theta in arange(0 * unit_deg, 359 * unit_deg, 5 * unit_deg):
            context.begin_path()
            context.move_to(x=r_1 * cos(theta), y=-r_1 * sin(theta))
            context.line_to(x=r_4 * cos(theta), y=-r_4 * sin(theta))
            context.stroke()

        # Mark fine scale of 1-degree intervals between circles 2 and 3
        for theta in arange(0 * unit_deg, 359.9 * unit_deg, 1 * unit_deg):
            context.begin_path()
            context.move_to(x=r_2 * cos(theta), y=-r_2 * sin(theta))
            context.line_to(x=r_3 * cos(theta), y=-r_3 * sin(theta))
            context.stroke()

        # Between circles 3 and 4 mark each constellation 10, 20, 30 degrees
        # Also, between circles 1 and 2, surround entire astrolabe with 0, 10, .. 90 degrees

        rt_1 = (r_1 + r_2) / 2
        rt_2 = (r_3 + r_4) / 2

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

            context.set_font_size(1.2)

            if theta_disp == 0:
                theta2 = theta
                context.text(text="0",
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=-1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)
            elif theta_disp == -180:
                theta2 = theta
                context.set_font_size(2.1)
                context.text(text="\u2720",
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=0, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)
            else:
                theta2 = theta - 0.2 * unit_deg
                context.text(text="{:.0f}".format(theta_disp / 10),
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)
                theta2 = theta + 0.2 * unit_deg
                context.text(text="{:.0f}".format(theta_disp % 10),
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=-1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)

            context.set_font_size(1.2)
            theta_disp = floor(theta / unit_deg + 380.01) % 30 + 10
            theta2 = theta - 0.2 * unit_deg
            context.text(text="{:.0f}".format(theta_disp / 10),
                         x=rt_2 * cos(theta2), y=-rt_2 * sin(theta2),
                         h_align=1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)
            theta2 = theta + 0.2 * unit_deg
            context.text(text="{:.0f}".format(theta_disp % 10),
                         x=rt_2 * cos(theta2), y=-rt_2 * sin(theta2),
                         h_align=-1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)

        # Write names of zodiacal constellations
        for i, item in enumerate(text[language]["zodiacal_constellations"]):
            i += 1
            name = "{} {}".format(item['name'], item['symbol'])
            context.circular_text(text=name,
                                  centre_x=0, centre_y=0, radius=(r_4 * 0.65 + r_5 * 0.35),
                                  azimuth=(-15 + 30 * i),
                                  spacing=1, size=1)

        # Between circles 5 and 10, display calendars for 1394 and 1974

        # Produce functions which interpolate the Tuckerman tables
        x_1394 = []
        y_1394 = []
        x_1974 = []
        y_1974 = []
        for line in open("raw_data/tuckerman.dat", "rt"):
            line = line.strip()

            # Ignore blank lines and comment lines
            if (len(line) == 0) or (line[0] == '#'):
                continue

            # Split line into words
            columns = [float(i) for i in line.split()]

            x_1394.append(calendar.julian_day(year=1394, month=int(columns[0]), day=int(columns[1]),
                                              hour=12, minute=0, sec=0))
            x_1974.append(calendar.julian_day(year=1974, month=int(columns[0]), day=int(columns[1]),
                                              hour=12, minute=0, sec=0))

            y_1394.append(30 * unit_deg * (columns[4] - 1) + columns[5] * unit_deg)
            y_1974.append(30 * unit_deg * (columns[6] - 1) + columns[7] * unit_deg)

        theta_1394 = scipy.interpolate.interp1d(x=x_1394, y=y_1394, kind='linear')
        theta_1974 = scipy.interpolate.interp1d(x=x_1974, y=y_1974, kind='linear')

        # Use Tuckerman table to mark 365 days around calendar.
        # Write numbers on the 10th, 20th and last day of each month

        rt_1 = (r_6 + r_7) / 2
        rt_2 = (r_8 + r_9) / 2
        last_theta = 30 * unit_deg * (10 - 1) + 9.4 * unit_deg

        for line in open("raw_data/tuckerman.dat"):
            line = line.strip()

            # Ignore blank lines and comment lines
            if (len(line) == 0) or (line[0] == "#"):
                continue

            m, d, interval, last, z1394, a1394, z1974, a1974 = [float(i) for i in line.split()]

            # Work out azimuth of given date in 1974 calendar
            theta = 30 * unit_deg * (z1974 - 1) + a1974 * unit_deg

            # Interpolate interval into number of days since last data point in table (normally five)
            if last_theta > theta:
                last_theta = last_theta - unit_rev
            for i in arange(0, interval - 0.1):
                theta_day = last_theta + (theta - last_theta) * (i + 1) / interval
                context.begin_path()
                context.move_to(x=r_7 * cos(theta_day), y=-r_7 * sin(theta_day))
                context.line_to(x=r_8 * cos(theta_day), y=-r_8 * sin(theta_day))
                context.stroke()
            last_theta = theta

            # Draw a marker line on calendar. Month ends get longer markers
            if last:
                context.begin_path()
                context.move_to(x=r_8 * cos(theta), y=-r_8 * sin(theta))
                context.line_to(x=r_10 * cos(theta), y=-r_10 * sin(theta))
                context.stroke()
            else:
                context.begin_path()
                context.move_to(x=r_8 * cos(theta), y=-r_8 * sin(theta))
                context.line_to(x=r_9 * cos(theta), y=-r_9 * sin(theta))
                context.stroke()

            # Label 10th and 20th day of month, and last day of month
            if ((d % 10) == 0) or (d > 26):
                context.set_font_size(1.0)
                theta2 = theta - 0.2 * unit_deg
                context.text(text="{:.0f}".format(d / 10),
                             x=rt_2 * cos(theta2), y=-rt_2 * sin(theta2),
                             h_align=1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)
                theta2 = theta + 0.2 * unit_deg
                context.text(text="{:.0f}".format(d % 10),
                             x=rt_2 * cos(theta2), y=-rt_2 * sin(theta2),
                             h_align=-1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)

            # Work out azimuth of given date in 1394 calendar
            theta = 30 * unit_deg * (z1394 - 1) + a1394 * unit_deg
            if last:
                context.begin_path()
                context.move_to(x=r_5 * cos(theta), y=-r_5 * sin(theta))
                context.line_to(x=r_7 * cos(theta), y=-r_7 * sin(theta))
                context.stroke()
            else:
                context.begin_path()
                context.move_to(x=r_6 * cos(theta), y=-r_6 * sin(theta))
                context.line_to(x=r_7 * cos(theta), y=-r_7 * sin(theta))
                context.stroke()

            # Label 10th and 20th day of month, and last day of month
            if ((d % 10) == 0) or (d > 26):
                context.set_font_size(0.75)
                theta2 = theta - 0.2 * unit_deg
                context.text(text="{:.0f}".format(d / 10),
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)
                theta2 = theta + 0.2 * unit_deg
                context.text(text="{:.0f}".format(d % 10),
                             x=rt_1 * cos(theta2), y=-rt_1 * sin(theta2),
                             h_align=-1, v_align=0, gap=0, rotation=-theta - 90 * unit_deg)

        # Label names of months
        for mn, (mlen, name) in enumerate(text[language]['months']):
            theta = theta_1974(calendar.julian_day(year=1974, month=mn + 1, day=mlen // 2, hour=12, minute=0, sec=0))
            context.circular_text(text=name, centre_x=0, centre_y=0, radius=r_9 * 0.65 + r_10 * 0.35,
                                  azimuth=theta / unit_deg,
                                  spacing=1, size=0.9)

            theta = theta_1394(calendar.julian_day(year=1394, month=mn + 1, day=mlen // 2, hour=12, minute=0, sec=0))
            context.circular_text(text=name, centre_x=0, centre_y=0, radius=r_5 * 0.65 + r_6 * 0.35,
                                  azimuth=theta / unit_deg,
                                  spacing=1, size=0.75)

        # Add significant dates between circles 10 and 12
        context.set_font_size(1.0)
        for line in open("raw_data/saints_days.dat"):
            line = line.strip()

            # Ignore blank lines and comment lines
            if (len(line) == 0) or (line[0] == "#"):
                continue

            d, m, name = line.split()

            day_week = floor(calendar.julian_day(year=1974, month=int(m), day=int(d), hour=12, minute=0, sec=0) -
                             calendar.julian_day(year=1974, month=1, day=1, hour=12, minute=0, sec=0)) % 7
            sunday_letter = "abcdefg"[day_week:day_week + 1]
            theta = theta_1974(calendar.julian_day(year=1974, month=int(m), day=int(d), hour=12, minute=0, sec=0))
            context.circular_text(text=name, centre_x=0, centre_y=0, radius=r_10 * 0.65 + r_11 * 0.35,
                                  azimuth=theta / unit_deg,
                                  spacing=1, size=1)
            context.circular_text(text=sunday_letter, centre_x=0, centre_y=0, radius=r_11 * 0.65 + r_12 * 0.35,
                                  azimuth=theta / unit_deg,
                                  spacing=1, size=1)

        # Shadow scale in middle of astrolabe
        context.begin_path()

        theta_a = 0 * unit_deg
        context.move_to(x=r_12 * cos(theta_a), y=-r_12 * sin(theta_a))
        context.line_to(x=r_13 * cos(theta_a), y=-r_13 * sin(theta_a))

        theta_b = - 45 * unit_deg
        context.move_to(x=r_12 * cos(theta_b), y=-r_12 * sin(theta_b))
        context.line_to(x=r_13 * cos(theta_b), y=-r_13 * sin(theta_b))

        theta_c = -135 * unit_deg
        context.move_to(x=r_12 * cos(theta_c), y=-r_12 * sin(theta_c))
        context.line_to(x=r_13 * cos(theta_c), y=-r_13 * sin(theta_c))

        theta_d = 180 * unit_deg
        context.move_to(x=r_12 * cos(theta_d), y=-r_12 * sin(theta_d))
        context.line_to(x=r_13 * cos(theta_d), y=-r_13 * sin(theta_d))
        context.move_to(x=r_12 * cos(theta_b), y=-r_12 * sin(theta_b))
        context.line_to(x=r_12 * cos(theta_b), y=0)
        context.move_to(x=r_12 * cos(theta_b), y=-r_12 * sin(theta_b))
        context.line_to(x=r_12 * cos(theta_c), y=-r_12 * sin(theta_c))
        context.move_to(x=r_12 * cos(theta_c), y=-r_12 * sin(theta_c))
        context.line_to(x=r_12 * cos(theta_c), y=0)
        context.move_to(x=0, y=-r_12 * sin(theta_c))
        context.line_to(x=0, y=r_13)
        context.move_to(x=0, y=-r_12)
        context.line_to(x=0, y=-r_13)

        rs1 = r_12 - 0.75 * d_12 / 2
        rs2 = rs1 - 0.75 * d_12
        context.move_to(x=rs1 * cos(theta_b), y=-rs1 * sin(theta_b))
        context.line_to(x=rs1 * cos(theta_b), y=0)
        context.move_to(x=rs1 * cos(theta_b), y=-rs1 * sin(theta_b))
        context.line_to(x=rs1 * cos(theta_c), y=-rs1 * sin(theta_c))
        context.move_to(x=rs1 * cos(theta_c), y=-rs1 * sin(theta_c))
        context.line_to(x=rs1 * cos(theta_c), y=0)
        context.move_to(x=rs2 * cos(theta_b), y=-rs2 * sin(theta_b))
        context.line_to(x=rs2 * cos(theta_b), y=0)
        context.move_to(x=rs2 * cos(theta_b), y=-rs2 * sin(theta_b))
        context.line_to(x=rs2 * cos(theta_c), y=-rs2 * sin(theta_c))
        context.move_to(x=rs2 * cos(theta_c), y=-rs2 * sin(theta_c))
        context.line_to(x=rs2 * cos(theta_c), y=0)

        context.stroke()

        context.set_font_size(0.64)
        context.text(text="UMBRA", x=-1 * unit_mm, y=-rs2 * sin(theta_c), h_align=1, v_align=-1, gap=0.7 * unit_mm,
                     rotation=0)
        context.text(text="UMBRA", x=rs2 * cos(theta_c), y=unit_mm, h_align=-1, v_align=-1, gap=0.7 * unit_mm,
                     rotation=pi / 2)
        context.text(text="RECTA", x=1 * unit_mm, y=-rs2 * sin(theta_c), h_align=-1, v_align=-1, gap=0.7 * unit_mm,
                     rotation=0)
        context.text(text="VERSA", x=rs2 * cos(theta_b), y=unit_mm, h_align=1, v_align=-1, gap=0.7 * unit_mm,
                     rotation=-pi / 2)
        context.text(text="ORIENS", x=-r_12 * 0.95, y=0, h_align=-1, v_align=-1, gap=0.8 * unit_mm, rotation=0)
        context.text(text="OCCIDENS", x=r_12 * 0.95, y=0, h_align=1, v_align=-1, gap=0.8 * unit_mm, rotation=0)

        r_label = (rs1 + rs2) / 2
        offset = 5 * unit_deg

        # Divisions of scale
        q = 90 * unit_deg
        for i in range(1, 12):
            rs = rs2 if (i % 4 == 0) else rs1
            theta = -atan(i / 12)
            context.begin_path()
            context.move_to(x=rs * cos(theta_b), y=-rs * cos(theta_b) * tan(theta))
            context.line_to(x=r_12 * cos(theta_b), y=-r_12 * cos(theta_b) * tan(theta))
            context.stroke()

            if i % 4 == 0:
                context.text(text="{:d}".format(i),
                             x=r_label * cos(theta_b), y=-r_label * cos(theta_b) * tan(theta - offset),
                             h_align=0, v_align=0, gap=0, rotation=-q - theta)

            theta = -atan(12 / i)
            context.begin_path()
            context.move_to(x=rs * sin(theta_b) / tan(theta), y=-rs * sin(theta_b))
            context.line_to(x=r_12 * sin(theta_b) / tan(theta), y=-r_12 * sin(theta_b))
            context.stroke()

            if i % 4 == 0:
                context.text(text="{:d}".format(i),
                             x=r_label * sin(theta_b) / tan(theta - offset), y=-r_label * sin(theta_b),
                             h_align=0, v_align=0, gap=0, rotation=-q - theta)

            theta = -2 * q - theta
            context.begin_path()
            context.move_to(x=rs * sin(theta_b) / tan(theta), y=-rs * sin(theta_b))
            context.line_to(x=r_12 * sin(theta_b) / tan(theta), y=-r_12 * sin(theta_b))
            context.stroke()

            if i % 4 == 0:
                context.text(text="{:d}".format(i),
                             x=r_label * sin(theta_b) / tan(theta + offset), y=-r_label * sin(theta_b),
                             h_align=0, v_align=0, gap=0, rotation=-q - theta)

            theta = -2 * q + atan(i / 12)
            context.begin_path()
            context.move_to(x=rs * cos(theta_c), y=-rs * cos(theta_c) * tan(theta))
            context.line_to(x=r_12 * cos(theta_c), y=-r_12 * cos(theta_c) * tan(theta))
            context.stroke()

            if i % 4 == 0:
                context.text(text="{:d}".format(i),
                             x=r_label * cos(theta_c), y=-r_label * cos(theta_c) * tan(theta + offset),
                             h_align=0, v_align=0, gap=0, rotation=-q - theta)

        theta = - 45 * unit_deg
        context.text(text="12", x=r_label * sin(theta_b) / tan(theta - offset), y=-r_label * sin(theta_b), h_align=0,
                     v_align=0, gap=0, rotation=-pi / 4)

        theta = -135 * unit_deg
        context.text(text="12", x=r_label * sin(theta_b) / tan(theta + offset), y=-r_label * sin(theta_b), h_align=0,
                     v_align=0, gap=0, rotation=pi / 4)

        # Unequal hours scale
        context.begin_path()
        context.circle(centre_x=0, centre_y=-r_12 / 2, radius=r_12 / 2)
        context.stroke()

        for theta in arange(15 * unit_deg, 75.1 * unit_deg, 15 * unit_deg):
            y_centre = r_12 * cos(theta) / 2 + r_12 * sin(theta) / 2 * tan(theta)
            arc_end = atan2(r_12 * sin(theta), r_12 * cos(theta) / 2 - r_12 * sin(theta) / 2 * tan(theta))

            context.begin_path()
            context.arc(centre_x=0, centre_y=-y_centre, radius=y_centre,
                        arc_from=arc_end - pi / 2, arc_to=-arc_end - pi / 2)
            context.stroke()

        # Finish up
        context.set_color(r=0, g=0, b=0)
        context.circular_text(text=text[language]['copyright'], centre_x=0, centre_y=0, radius=r_12 - 2 * unit_mm,
                              azimuth=270, spacing=1, size=0.7)


# Do it right away if we're run as a script
if __name__ == "__main__":
    # Fetch command line arguments passed to us
    arguments = fetch_command_line_arguments(default_filename=MotherBack().default_filename())

    # Render the back of the mother
    MotherBack(settings={
        'latitude': arguments['latitude'],
        'language': 'en'
    }).render_to_file(
        filename=arguments['filename'],
        img_format=arguments['img_format']
    )
