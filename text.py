# text.py
# -*- coding: utf-8 -*-
#
# The python script in this file makes the various parts of a model astrolabe.
#
# Copyright (C) 2010-2018 Dominic Ford <dcf21-www_dcford.org.uk>
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

text = {
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
            "constellation_translations": {
            },
            "url": "https://in-the-sky.org/astrolabe/index.html",
            "copyright": "\u00A9 Dominic Ford 2018",
            "climate_latitude": "Climate prepared for latitude {:02d}{:s}"
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
            "constellation_translations": {
                "Andromeda": "Andromède",
                "Antlia": "Antlia",
                "Apus": "Apus",
                "Aquarius": "Verseau",
                "Aquila": "Aigle",
                "Ara": "Autel",
                "Aries": "Bélier",
                "Auriga": "Cocher",
                "Boötes": "Bouvier",
                "Caelum": "Burin",
                "Camelopardalis": "Girafe",
                "Cancer": "Cancer",
                "Canes_Venatici": "Chiens_de_chasse",
                "Canis_Major": "Grand_Chien",
                "Canis_Minor": "Petit_Chien",
                "Capricornus": "Capricorne",
                "Carina": "Carène",
                "Cassiopeia": "Cassiopée",
                "Centaurus": "Centaure",
                "Cepheus": "Céphée",
                "Cetus": "Baleine",
                "Chamaeleon": "Chamaeleon",
                "Circinus": "Circinus",
                "Columba": "Colombe",
                "Coma_Berenices": "Chevelure_de_Bérénice",
                "Corona_Australis": "Couronne_australe",
                "Corona_Borealis": "Couronne_boréale",
                "Corvus": "Corbeau",
                "Crater": "Coupe",
                "Crux": "Croix_du_Sud",
                "Cygnus": "Cygne",
                "Delphinus": "Dauphin",
                "Dorado": "Dorado",
                "Draco": "Dragon",
                "Equuleus": "Petit_Cheval",
                "Eridanus": "Éridan",
                "Fornax": "Fourneau",
                "Gemini": "Gémeaux",
                "Grus": "Grue",
                "Hercules": "Hercule",
                "Horologium": "Horloge",
                "Hydra": "Hydre",
                "Hydrus": "Hydrus",
                "Indus": "Indien",
                "Lacerta": "Lézard",
                "Leo": "Lion",
                "Leo_Minor": "Petit_Lion",
                "Lepus": "Lièvre",
                "Libra": "Balance",
                "Lupus": "Loup",
                "Lynx": "Lynx",
                "Lyra": "Lyre",
                "Mensa": "Mensa",
                "Microscopium": "Microscope",
                "Monoceros": "Licorne",
                "Musca": "Musca",
                "Norma": "Règle",
                "Octans": "Octans",
                "Ophiuchus": "Serpentaire",
                "Orion": "Orion",
                "Pavo": "Pavo",
                "Pegasus": "Pégase",
                "Perseus": "Persée",
                "Phoenix": "Phénix",
                "Pictor": "Peintre",
                "Pisces": "Poissons",
                "Piscis_Austrinus": "Poisson_austral",
                "Puppis": "Poupe",
                "Pyxis": "Boussole",
                "Reticulum": "Réticule",
                "Sagitta": "Flèche",
                "Sagittarius": "Sagittaire",
                "Scorpius": "Scorpion",
                "Sculptor": "Sculpteur",
                "Scutum": "Écu_de_Sobieski",
                "Serpens": "Serpent",
                "Sextans": "Sextant",
                "Taurus": "Taureau",
                "Telescopium": "Télescope",
                "Triangulum": "Triangle",
                "Triangulum_Australe": "Triangulum_Australe",
                "Tucana": "Toucan",
                "Ursa_Major": "Grande_Ourse",
                "Ursa_Minor": "Petite_Ourse",
                "Vela": "Voiles",
                "Virgo": "Vierge",
                "Volans": "Volans",
                "Vulpecula": "Petit_Renard"
            },
            "url": "https://in-the-sky.org/astrolabe/index.html",
            "copyright": "\u00A9 Dominic Ford 2018",
            "climate_latitude": "Climate prepared for latitude {:02d}{:s}"
        }
}
