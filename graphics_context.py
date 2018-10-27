# graphics_context.py
# -*- coding: utf-8 -*-
#
# The python script in this file makes the various parts of a model astrolabe.
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

"""
A thin wrapper to produce vector graphics using cairo.
"""

from math import sin, cos

import cairocffi as cairo
from constants import unit_deg, font_size_base, dots_per_inch


class GraphicsPage:
    """
    A thin wrapper to produce vector graphics using cairo. This class represents a page / image file we are going
    to draw onto.
    """

    def __init__(self,
                 img_format="png",
                 output="page",
                 width=0.15,
                 height=0.15,
                 dots_per_inch=dots_per_inch):
        """
        A thin wrapper to produce vector graphics using cairo. This class represents a page / image file we are going
        to draw onto.

        :param img_format:
            The image format we are to produce.
        :type img_format:
            str
        :param output:
            The filename of the image file we are to produce, without a file type suffix
        :type output:
            str
        :param width:
            The width of the page, metres
        :type width:
            float
        :param height:
            The height of the page, metres
        :type height:
            float
        :param dots_per_inch:
            The dots per inch resolution to render this page
        :type dots_per_inch:
            float
        """

        self.format = img_format
        self.output = "{}.{}".format(output, img_format)
        self.dots_per_metre = dots_per_inch * 39.370079
        self.width = int(width * self.dots_per_metre)
        self.height = int(height * self.dots_per_metre)

        if self.format == "pdf":
            self.surface = cairo.PDFSurface(self.output, self.width, self.height)
        elif self.format == "png":
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        elif self.format == "svg":
            self.surface = cairo.SVGSurface(self.output, self.width, self.height)
        else:
            assert False, "Unknown image output format {}".format(self.format)

    def __del__(self):
        """
        Save the canvas we have drawn to disk

        :return:
            None
        """

        print("Creating file <{}>".format(self.output))

        if self.format == "pdf":
            self.surface.show_page()
        elif self.format == "png":
            self.surface.write_to_png(self.output)
        elif self.format == "svg":
            self.surface.show_page()
        else:
            assert False, "Unknown image output format {}".format(self.format)

        del self.surface

    @staticmethod
    def supported_formats():
        return "pdf", "png", "svg"


class GraphicsContext:
    """
    A thin wrapper to produce vector graphics using cairo. This class provides a drawing context that we can use to
    draw a figure onto a page.
    """

    def __init__(self,
                 page,
                 offset_x=0,
                 offset_y=0,
                 rotation=0):
        """
        A thin wrapper to produce vector graphics using cairo. This class provides a drawing context that we can use to
        draw a figure onto a page.

        :param page:
            The GraphicsPage we are going to draw onto
        :param offset_x:
            The offset of this drawing from (0,0) on the page
        :param offset_y:
            The offset of this drawing from (0,0) on the page
        :param rotation:
            The rotation of this drawing
        """

        assert isinstance(page, GraphicsPage)

        self.context = cairo.Context(target=page.surface)
        self.context.scale(sx=page.dots_per_metre, sy=page.dots_per_metre)
        self.context.translate(tx=offset_x, ty=offset_y)
        self.context.rotate(radians=rotation * unit_deg)

    def begin_path(self):
        self.context.new_path()

    def move_to(self, x, y):
        self.context.move_to(x=x, y=y)

    def line_to(self, x, y):
        self.context.line_to(x=x, y=y)

    def close_path(self):
        self.context.close_path()

    def stroke(self):
        self.context.stroke_preserve()

    def fill(self):
        self.context.fill_preserve()

    def arc(self, centre_x, centre_y, radius, arc_from, arc_to):
        self.context.arc(xc=centre_x, yc=centre_y, radius=radius, angle1=arc_from * unit_deg, angle2=arc_to * unit_deg)

    def circle(self, centre_x, centre_y, radius):
        self.arc(centre_x=centre_x, centre_y=centre_y, radius=radius, arc_from=0, arc_to=360)

    def rectangle(self, x0, y0, x1, y1):
        self.context.rectangle(x=x0, y=y0, width=x1 - x0, height=y1 - y0)

    def set_font_size(self, font_size):
        """
        Change the font size used to render text.

        :param font_size:
            Font size, relative to default
        :return:
            None
        """
        self.context.set_font_size(font_size)

    def text(self, text, x, y, h_align=0, v_align=0, gap=0, rotation=0):
        """
        Add a text string to the drawing canvas.
        :param text:
            The string to write
        :param x:
            The horizontal position of the string
        :param y:
            The vertical position of the string
        :param h_align:
            The horizontal alignment of the string: -1 left; 0 centred; 1 right
        :param v_align:
            The vertical alignment of the string: -1 top; 0 centred; 1 bottom
        :param gap:
            Leave a gap between the anchor point (x,y) and where the text is rendered
        :param rotation:
            The rotation angle of the text, degrees
        :return:
            None
        """

        text = str(text)
        extent = self.measure_text(text=text)

        # Cairo places top-left of text at specified point. For other alignments, we calculate where this point will be
        offset_x = 0
        offset_y = 0
        if h_align >= 0:
            offset_x -= extent['width'] / 2
        if h_align > 0:
            offset_x -= extent['width'] / 2
        if v_align >= 0:
            offset_y += extent['height'] / 2
        if v_align > 0:
            offset_y += extent['height'] / 2

        # Now draw text
        self.context.save()
        self.context.translate(tx=x - gap * h_align, ty=y - gap * v_align)
        self.context.rotate(radians=rotation * unit_deg)
        self.context.translate(tx=offset_x, ty=offset_y)
        self.context.move_to(x=0, y=0)
        self.context.show_text(text=text)
        self.context.restore()

    def measure_text(self, text):
        """
        Measure the dimensions of a string of text, as it would be rendered in the currently-selected font.
        :param text:
            Text string to render
        :return:
            Dictionary of size information about the text string
        """
        (x, y, width, height, dx, dy) = self.context.text_extents(text=text)
        return {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "dx": dx,
            "dy": dy
        }

    def circular_text(self, text, centre_x, centre_y, radius, azimuth, spacing, size):
        """
        Write a text string around a circular path.

        :param text:
            The string that we are to write
        :param centre_x:
            The horizontal position of the centre of the circle we are to write the text around
        :param centre_y:
            The vertical position of the centre of the circle we are to write the text around
        :param radius:
            The radius of the circular path we are to write the text around / pixel
        :param azimuth:
            The angle, in degrees, where the text string is to be centred. Measured clockwise from straight up.
        :param spacing:
            The spacing between the letters.
        :param size:
            The font size to use
        :return:
            None
        """

        self.set_font_size(size * font_size_base)

        # First calculate total length of text
        text_width = 0
        for char in text:
            text_width += float(self.measure_text(text=char)['width'])

        # Work out the angular span of the text around the specified circular path
        text_angular_width = text_width / radius / unit_deg

        # Work out the azimuth at which we need to start, in order to have centre of text at specified azimuth
        current_azimuth = azimuth + spacing * text_angular_width / 2

        # Then render text, one character at a time
        for char in text:
            character_width = float(self.measure_text(text=char)['width'])
            current_azimuth -= character_width / 2 * spacing / radius / unit_deg
            self.text(text=char,
                      x=centre_x + radius * cos(current_azimuth),
                      y=centre_y + radius * sin(current_azimuth),
                      rotation=current_azimuth - 90 * unit_deg
                      )

        # Done
        return


class BaseComponent:
    """
    A class wrapping a piece of code used to draw a single component of the model.
    """

    def __init__(self, settings=None):
        """
        A class wrapping a piece of code used to draw a single component of the model.

        :param settings:
            Settings used in the rendering of this component
        """

        if settings is None:
            settings = {}
        self.settings = settings

    def render_to_page(self, page, offset_x=0, offset_y=0, rotation=0):
        """
        Render this component onto a Page object.

        :param page:
            The GraphicsPage we are going to draw onto
        :param offset_x:
            The offset of this drawing from (0,0) on the page
        :param offset_y:
            The offset of this drawing from (0,0) on the page
        :param rotation:
            The rotation of this drawing
        """

        # Make sure that the page we're going to draw onto is of the correct type
        assert isinstance(page, GraphicsPage)

        # Create a drawing context for drawing onto this page
        context = GraphicsContext(page=page, offset_x=offset_x, offset_y=offset_y, rotation=rotation)

        # Render this item
        self.do_rendering(settings=self.settings, context=context)

        # Clean up
        del context

    def render_to_file(self, filename=None, img_format="svg", dots_per_inch=dots_per_inch):
        """
        Renders the component to an image file.

        :param filename:
            The filename of the image file to create (without file type stub)
        :param img_format:
            The format of the image file to create
        :param dots_per_inch:
            The dots per inch resolution to render this page
        :type dots_per_inch:
            float
        :return:
            BaseComponent instance
        """

        # Look up the bounding box of the item we're about to draw
        bounding_box = self.bounding_box()

        # If no filename is specified, then individual derived classes should specify a default
        if filename is None:
            filename = self.default_filename()

        # Create a graphics page large enough to hold this item
        page = GraphicsPage(img_format=img_format, output=filename,
                            width=bounding_box['x_max'] - bounding_box['x_min'],
                            height=bounding_box['y_max'] - bounding_box['y_min'],
                            dots_per_inch=dots_per_inch
                            )

        # Render the item
        self.render_to_page(page=page,
                            offset_x=bounding_box['x_min'],
                            offset_y=bounding_box['y_min'])

        # Clean up
        del page

    def render_all_formats(self, filename=None, dots_per_inch=dots_per_inch):
        """
        Quick shortcut to render this component in all the standard image formats.

        :param filename:
            The filename of the image file to create (without file type stub)
        :param dots_per_inch:
            The dots per inch resolution to render this page
        :type dots_per_inch:
            float
        :return:
            None
        """

        # Produce each image format in turn
        for img_format in GraphicsPage.supported_formats():
            # Render the item
            self.render_to_file(filename=filename,
                                img_format=img_format,
                                dots_per_inch=dots_per_inch)

    def bounding_box(self):
        """
        This method is required to report the bounding box of the canvas area used by this item.

        :return:
            Dictionary with the elements 'x_min', 'x_max', 'y_min and 'y_max' set to the canvas area required.
        """
        raise NotImplementedError("Derived classes of type <BaseComponent> must implement a method <bounding_box> "
                                  "which reports the area of canvas they require.")

    def default_filename(self):
        """
        This method is required to report a default filename to use for this item, without file type suffix.

        :return:
            string
        """
        raise NotImplementedError("Derived classes of type <BaseComponent> must implement a method "
                                  "<default_filename> which report a default filename to use for this item, without "
                                  "file type suffix.")

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
        raise NotImplementedError("Derived classes of type <BaseComponent> must implement a method <do_rendering> "
                                  "to draw the component.")


class CompositeComponent(BaseComponent):
    """
    A class allowing multiple components to be overlaid on a single canvas
    """

    def __init__(self, components, settings=None):
        self.components = components
        super(CompositeComponent, self).__init__(settings=settings)

    def default_filename(self):
        return "composite_page"

    def bounding_box(self):
        """
        Work out overall bounding box of all items when constituent components are overlaid.
        """

        bounding_boxes = [item.bounding_box() for item in self.components]

        return {
            'x_min': min([item['x_min'] for item in bounding_boxes]),
            'x_max': max([item['x_max'] for item in bounding_boxes]),
            'y_min': min([item['y_min'] for item in bounding_boxes]),
            'y_max': max([item['y_max'] for item in bounding_boxes]),
        }

    def do_rendering(self, settings, context):
        """
        Render each of the sub-components we are overlaying in turn.

        :param settings:
            A dictionary of settings required by the renderer.
        :param context:
            A GraphicsContext object to use for drawing
        :return:
            None
        """

        for item in self.components:
            item.do_rendering(settings=settings, context=context)
