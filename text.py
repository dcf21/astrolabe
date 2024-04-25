# text.py
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

# A list of text strings, which we can render in various languages

from typing import Dict

text: Dict[str, dict] = {
    "en":
        {
            "months": [
                [31, "JANUARY"],
                [28, "FEBRUARY"],
                [31, "MARCH"],
                [30, "APRIL"],
                [31, "MAY"],
                [30, "JUNE"],
                [31, "JULY"],
                [31, "AUGUST"],
                [30, "SEPTEMBER"],
                [31, "OCTOBER"],
                [30, "NOVEMBER"],
                [31, "DECEMBER"]
            ],
            "zodiacal_constellations": [
                {"name": "Aries", "symbol": "\u2648"},
                {"name": "Taurus", "symbol": "\u2649"},
                {"name": "Gemini", "symbol": "\u264a"},
                {"name": "Cancer", "symbol": "\u264b"},
                {"name": "Leo", "symbol": "\u264c"},
                {"name": "Virgo", "symbol": "\u264d"},
                {"name": "Libra", "symbol": "\u264e"},
                {"name": "Scorpio", "symbol": "\u264f"},
                {"name": "Sagittarius", "symbol": "\u2650"},
                {"name": "Capricornus", "symbol": "\u2651"},
                {"name": "Aquarius", "symbol": "\u2652"},
                {"name": "Pisces", "symbol": "\u2653"},
            ],
            "url": "https://in-the-sky.org/astrolabe/index.html",
            "copyright": "\u00A9 Dominic Ford 2010\u20132024",
            "climate_latitude": "Climate prepared for latitude {:02d}{:s}",
            "name": "Name",
            "directions": ["N", "NNW", "NW", "WNW", "W", "WSW", "SW", "SSW",
                           "S", "SSE", "SE", "ESE", "E", "ENE", "NE", "NNE"],
            "midnight": "Midnight"
        },
    "fr":
        {
            "months": [
                [31, "JANVIER"],
                [28, "FÉVRIER"],
                [31, "MARS"],
                [30, "AVRIL"],
                [31, "MAI"],
                [30, "JUIN"],
                [31, "JUILLET"],
                [31, "AOÛT"],
                [30, "SEPTEMBRE"],
                [31, "OCTOBRE"],
                [30, "NOVEMBRE"],
                [31, "DÉCEMBRE"]
            ],
            "zodiacal_constellations": [
                {"name": "Bélier", "symbol": "\u2648"},
                {"name": "Taureau", "symbol": "\u2649"},
                {"name": "Gémeaux", "symbol": "\u264a"},
                {"name": "Cancer", "symbol": "\u264b"},
                {"name": "Lion", "symbol": "\u264c"},
                {"name": "Vierge", "symbol": "\u264d"},
                {"name": "Balance", "symbol": "\u264e"},
                {"name": "Scorpion", "symbol": "\u264f"},
                {"name": "Sagittaire", "symbol": "\u2650"},
                {"name": "Capricorne", "symbol": "\u2651"},
                {"name": "Verseau", "symbol": "\u2652"},
                {"name": "Poissons", "symbol": "\u2653"},
            ],
            "url": "https://in-the-sky.org/astrolabe/index.html",
            "copyright": "\u00A9 Dominic Ford 2010\u20132024",
            "climate_latitude": "Climate prepared for latitude {:02d}\u00b0{:s}",
            "name": "Nom",
            "directions": ["N", "NNO", "NO", "ONO", "O", "OSO", "SO", "SSO",
                           "S", "SSE", "SE", "ESE", "E", "ENE", "NE", "NNE"],
            "midnight": "Minuit"
        },
    "sv":
        {
            "months": [
                [31, "JANUARI"],
                [28, "FÉBRUARI"],
                [31, "MARS"],
                [30, "APRIL"],
                [31, "MAJ"],
                [30, "JUNI"],
                [31, "JULI"],
                [31, "AUGUSTI"],
                [30, "SEPTEMBER"],
                [31, "OKTOBER"],
                [30, "NOVEMBER"],
                [31, "DECEMBER"]
            ],
            "zodiacal_constellations": [
                {"name": "Väduren", "symbol": "\u2648"},
                {"name": "Oxen", "symbol": "\u2649"},
                {"name": "Tvillingarna", "symbol": "\u264a"},
                {"name": "Kräftan", "symbol": "\u264b"},
                {"name": "Lejonet", "symbol": "\u264c"},
                {"name": "Jungfrun", "symbol": "\u264d"},
                {"name": "Vågen", "symbol": "\u264e"},
                {"name": "Skorpionen", "symbol": "\u264f"},
                {"name": "Skytten", "symbol": "\u2650"},
                {"name": "Stenbocken", "symbol": "\u2651"},
                {"name": "Vattumannen", "symbol": "\u2652"},
                {"name": "Fiskarna", "symbol": "\u2653"},
            ],
            "url": "https://in-the-sky.org/astrolabe/index.html",
            "copyright": "\u00A9 Dominic Ford 2010\u20132024",
            "climate_latitude": "Climate prepared for latitude {:02d}\u00b0{:s}",
            "name": "Namn",
            "directions": ["N", "NNV", "NV", "VNV", "V", "VSV", "SV", "SSV",
                           "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"],
            "midnight": "Midnight"
        },
    "de":
        {
            "months": [
                [31, "JANUAR"],
                [28, "FEBRUAR"],
                [31, "MÄRZ"],
                [30, "APRIL"],
                [31, "MAI"],
                [30, "JUNI"],
                [31, "JULI"],
                [31, "AUGUST"],
                [30, "SEPTEMBER"],
                [31, "OKTOBER"],
                [30, "NOVEMBER"],
                [31, "DEZEMBER"]
            ],
            "zodiacal_constellations": [
                {"name": "Widder", "symbol": "\u2648"},
                {"name": "Stier", "symbol": "\u2649"},
                {"name": "Zwillinge", "symbol": "\u264a"},
                {"name": "Krebs", "symbol": "\u264b"},
                {"name": "Löwe", "symbol": "\u264c"},
                {"name": "Jungfrau", "symbol": "\u264d"},
                {"name": "Waage", "symbol": "\u264e"},
                {"name": "Scorpion", "symbol": "\u264f"},
                {"name": "Schütze", "symbol": "\u2650"},
                {"name": "Steinbock", "symbol": "\u2651"},
                {"name": "Wassermann", "symbol": "\u2652"},
                {"name": "Fische", "symbol": "\u2653"},
            ],
            "url": "https://in-the-sky.org/astrolabe/index.html",
            "copyright": "\u00A9 Dominic Ford 2010\u20132024",
            "climate_latitude": "Klima vorbereited für geographische Breite {:02d}{:s}",
            "name": "Name",
            "directions": ["N", "NNW", "NW", "WNW", "W", "WSW", "SW", "SSW",
                           "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"],
            "midnight": "Mitternacht"
        }
}
