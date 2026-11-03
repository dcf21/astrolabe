## Make your own cardboard model astrolabe

This repository contains Python scripts that can be used to produce a cardboard cut-and-glue kit to make your own model astrolabe.

### Introduction

Astrolabes are elaborate astronomical instruments, combining a mechanical model of the sky's rotation with a simple sight, which can be used to make observations of the elevation of objects above the horizon. Put together, these tools allow the user to tell the time, identify objects in the sky, and predict when objects will rise and set.

In the Middle Ages, astrolabes were the most sophisticated astronomical instruments in widespread use, a position which they held for nearly two thousand years, from the time of their invention by Hipparchus (c. 190–120 BCE) until the turn of the seventeenth century. They only fell out of use around the time that the telescope was invented in 1609, as astronomers began to require more precise tools.

Today, the curious astronomer who wants to learn more about medieval observing practice may find it hard to find a specimen to play with. Historical examples are highly valuable, and usually found only in glass cases in museums. To solve this problem, I have created a cardboard cut-and-glue kit which you can download and print to make your own model astrolabe.

The design presented here is based upon one described by the English poet Geoffrey Chaucer in his *Treatise on the astrolabe*, published in 1391. In a series of three papers published in 1975–6, American historian Sigmund Eisner provided detailed geometric instructions for recreating Chaucer's astrolabe, which I follow closely.

See <https://in-the-sky.org/astrolabe/index.php> for more information, including detailed assembly instructions.

### Getting started

To make astrolabe models for all latitudes, at five degree intervals, run the shell script `main_astrolabe.sh`.

### Running in Docker

The scripts need Python 3 with the `cairocffi`, `numpy` and `scipy` packages,
and LaTeX to assemble the final PDF documents. Rather than installing these
yourself, you can run the scripts inside a Docker container, using the
`Dockerfile` and `docker-compose.yml` in this repository. The container uses
Python 3.14 on Debian.

To build the Docker image, and then make the astrolabe models inside a
container, run:

```
docker compose build
docker compose run --rm python
```

This runs `main_astrolabe.sh --theme default` inside the container, and removes
the container when it finishes. Making models for every latitude takes several
minutes. The repository directory is shared with the container, so the output
appears in the `output` directory, replacing any previous output.

The container runs as root, so the files it creates will be owned by root. To
create them as your own user instead, run:

```
docker compose run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp python
```

### Caveat

The astrolabe, as a medieval instrument, was never intended to be used close to the equator. It is not possible to make astrolabes for latitudes between 15&deg;N and 15&deg;S, as the celestial pole is too close to the horizon.

## Author

This code was developed by Dominic Ford <https://dcford.org.uk>. It is distributed under the Gnu General Public License V3.

