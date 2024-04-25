# settings.py
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
Define a common command-line interface which is shared between all the scripts.
"""

import argparse
from typing import Dict, Union


def fetch_command_line_arguments(default_filename: str = '') -> Dict[str, Union[int, str]]:
    """
    Read input parameters from the command line

    :return:
        Dictionary of command-line arguments
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--latitude', dest='latitude', type=int, default=52,
                        help="The latitude to create a astrolabe for.")
    parser.add_argument('--format', dest='img_format', choices=["pdf", "png", "svg"], default="png",
                        help="The image format to create.")
    parser.add_argument('--output', dest='filename', default=default_filename,
                        help="Filename for output, without a file type suffix.")
    parser.add_argument('--theme', dest='theme', choices=["default", "dark"], default="default",
                        help="Color theme to be used in the astrolabe.")
    args = parser.parse_args()

    return {
        "latitude": args.latitude,
        "img_format": args.img_format,
        "filename": args.filename,
        "theme": args.theme
    }
