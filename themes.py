# theme.py
# -*- coding: utf-8 -*-
#
# The python script in this file defines the available themes for the astrolabe.
#
# Copyright (C) 2019 André Werlang <https://dcford.org.uk/>
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

from typing import Dict, Tuple

themes: Dict[str, Dict[str, Tuple[float, float, float, float]]] = {
    "default":
        {
            "background": (1, 1, 1, 0),
            "text": (0, 0, 0, 1),
            "lines": (0, 0, 0, 1),
            "stick_figures": (0.75, 0.75, 0.75, 1),
            "alt_az": (0.7, 0.7, 0.7, 1)
        }
}
