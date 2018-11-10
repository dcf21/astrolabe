#!/bin/bash
# main_astrolabe.sh
# -*- coding: utf-8 -*-
#
# The bash script in this file makes the various parts of a model astrolabe.
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

# Delete any previous output from running this script
rm -Rf __pycache__ *.pyc output
rm -Rf doc/*.aux doc/*.dvi doc/*.log doc/*.pdf doc/*.ps doc/tmp doc/*.out

# Run the python 3 script which generates astrolabe models for a wide range of latitudes
python3 astrolabe.py

# Clean up temporary files which get made along the way
rm -Rf __pycache__ *.pyc
rm -Rf doc/*.aux doc/*.dvi doc/*.log doc/*.pdf doc/*.ps doc/tmp doc/*.out
