# constants.py
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
The file contains global settings for the astrolabe.
"""

from math import pi

# Units
dots_per_inch = 200

unit_m = 1.
unit_cm = 1. / 100
unit_mm = 1. / 1000

# Angle conversion
unit_deg = float(pi / 180)
unit_rev = 2. * pi

# Margins around output
margin_fraction = 1.02

# Outer radius of astrolabe
r_1 = 8.5 * unit_cm

# Distance between circles drawn on back of mother
d_12 = 0.07 * r_1

# Font size
font_size_base = 3.2 * unit_mm
line_width_base = 0.2 * unit_mm

# Size of tab into which climate slots
tab_size = 5 * unit_deg

# Scaling factor for size of hole in middle of astrolabe
centre_scaling = 1 / 2.5 * 0.6

# Inclination of the ecliptic
inclination_ecliptic = 23.5
