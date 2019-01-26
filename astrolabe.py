#!/usr/bin/python3
# astrolabe.py
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
This is the top level script for drawing all the parts needed to build astrolabes which work at a range of
different latitudes. They are rendered in PDF, SVG and PNG image formats.

Additionally, we use LaTeX to build a summary document for each latitude, which includes all of the parts needed
to build an astrolabe for that latitude, and instructions as to how to put them together.
"""

import os
import subprocess
import time

import text
from climate import Climate
from graphics_context import GraphicsPage, CompositeComponent
from mother_back import MotherBack
from mother_front import MotherFront
from rete import Rete
from rule import Rule
from settings import fetch_command_line_arguments

# Create clean output directory
os.system("rm -Rf output")
os.system("mkdir -p output/astrolabes output/astrolabe_parts")

arguments = fetch_command_line_arguments()
theme = arguments['theme']

# Render astrolabe in all available languages
for language in text.text:

    # Render climates for latitudes at 5-degree spacings from 10 deg -- 85 deg, plus 52N
    for latitude in list(range(-80, 90, 5)) + [52]:

        # Do not make equatorial astrolabes, as they don't really work
        if -10 < latitude < 10:
            continue

        # Boolean flag for which hemisphere we're in
        southern = latitude < 0

        # A dictionary of common substitutions
        subs = {
            "dir_parts": "output/astrolabe_parts",
            "dir_out": "output/astrolabes",
            "abs_lat": abs(latitude),
            "ns": "S" if southern else "N",
            "lang": language,
            "lang_short": "" if language == "en" else "_{}".format(language)
        }

        settings = {
            'language': language,
            'latitude': latitude,
            'theme': theme
        }

        # Render the parts of the astrolabe that do not change with geographic location
        MotherFront(settings=settings).render_all_formats(
            filename="{dir_parts}/mother_front_{abs_lat:02d}{ns}_{lang}".format(**subs)
        )

        MotherBack(settings=settings).render_all_formats(
            filename="{dir_parts}/mother_back_{abs_lat:02d}{ns}_{lang}".format(**subs)
        )

        Rete(settings=settings).render_all_formats(
            filename="{dir_parts}/rete_{abs_lat:02d}{ns}_{lang}".format(**subs)
        )

        Rule(settings=settings).render_all_formats(
            filename="{dir_parts}/rule_{abs_lat:02d}{ns}_{lang}".format(**subs)
        )

        # Render the climate of the astrolabe
        Climate(settings=settings).render_all_formats(
            filename="{dir_parts}/climate_{abs_lat:02d}{ns}_{lang}".format(**subs)
        )

        # Make combined mother and climate
        for img_format in GraphicsPage.supported_formats():
            CompositeComponent(
                settings=settings,
                components=[
                    MotherFront(settings=settings),
                    Climate(settings=settings)
                ]
            ).render_all_formats(
                filename="{dir_parts}/mother_front_combi_{abs_lat:02d}{ns}_{lang}".format(**subs)
            )

        # Copy the PDF versions of the components of this astrolabe into LaTeX's working directory, to produce a
        # PDF file containing all the parts of this astrolabe
        os.system("mkdir -p doc/tmp")
        os.system("cp {dir_parts}/mother_back_{abs_lat:02d}{ns}_{lang}.pdf doc/tmp/mother_back.pdf".format(**subs))
        os.system(
            "cp {dir_parts}/mother_front_combi_{abs_lat:02d}{ns}_{lang}.pdf doc/tmp/mother_front.pdf".format(**subs))
        os.system("cp {dir_parts}/rete_{abs_lat:02d}{ns}_{lang}.pdf doc/tmp/rete.pdf".format(**subs))
        os.system("cp {dir_parts}/rule_{abs_lat:02d}{ns}_{lang}.pdf doc/tmp/rule.pdf".format(**subs))

        with open("doc/tmp/lat.tex", "wt") as f:
            f.write(r"${abs_lat:d}^\circ${ns}".format(**subs))

        # Wait for cairo to wake up and close the files
        time.sleep(1)

        # Build LaTeX documentation
        for build_pass in range(3):
            subprocess.check_output("cd doc ; pdflatex astrolabe.tex", shell=True)
        os.system("mv doc/astrolabe.pdf {dir_out}/astrolabe_{abs_lat:02d}{ns}_{lang}.pdf".format(**subs))

        # For the English language astrolabe, create a symlink with no language suffix in the filename
        if language == "en":
            os.system("ln -s astrolabe_{abs_lat:02d}{ns}_en.pdf "
                      "{dir_out}/astrolabe_{abs_lat:02d}{ns}.pdf".format(**subs))

        # Clean up the rubbish that LaTeX leaves behind
        os.system("cd doc ; rm -f *.aux *.log *.dvi *.ps *.pdf")
