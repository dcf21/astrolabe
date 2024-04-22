# graphics_context.py
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
A thin wrapper to produce vector graphics using cairo.
"""

import logging

from math import pi, sin, cos

from typing import Dict, List, Optional, Sequence

import cairocffi as cairo
from constants import unit_deg, unit_mm, font_size_base, line_width_base, dots_per_inch


class GraphicsPage:
    """
    A thin wrapper to produce vector graphics using cairo. This class represents a page / image file we are going
    to draw onto.
    """

    def __init__(self,
                 img_format: str = "png",
                 output: str = "page",
                 width: float = 0.15,
                 height: float = 0.15,
                 dots_per_inch: float = dots_per_inch):
        """
        A thin wrapper to produce vector graphics using cairo. This class represents a page / image file we are going
        to draw onto.

        :param img_format:
            The image format we are to produce.
        :param output:
            The filename of the image file we are to produce, without file type suffix
        :param width:
            The width of the page, metres
        :param height:
            The height of the page, metres
        :param dots_per_inch:
            The dots per inch resolution to render this page
        """

        # PDF surfaces are always measured in points
        if img_format in ("pdf", "svg"):
            dots_per_inch = 72.

        self.format: str = img_format
        self.output: str = "{}.{}".format(output, img_format)
        self.dots_per_metre: float = dots_per_inch * 39.370079
        self.width: int = int(width * self.dots_per_metre)  # pixels
        self.height: int = int(height * self.dots_per_metre)  # pixels

        self.surface: Optional[cairo.Surface] = None
        if self.format == "pdf":
            self.surface = cairo.PDFSurface(self.output, self.width, self.height)
        elif self.format == "png":
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        elif self.format == "svg":
            self.surface = cairo.SVGSurface(self.output, self.width, self.height)
        else:
            assert False, "Unknown image output format {}".format(self.format)

    def __del__(self) -> None:
        """
        Save the canvas we have drawn to disk

        :return:
            None
        """

        # Protect against being called twice
        if self.surface is None:
            return

        logging.info("Creating file <{}>".format(self.output))

        if self.format == "pdf":
            self.surface.show_page()
        elif self.format == "png":
            self.surface.write_to_png(self.output)
        elif self.format == "svg":
            self.surface.show_page()
        else:
            assert False, "Unknown image output format {}".format(self.format)

        # Clean up
        self.surface.finish()
        self.surface = None

    def __enter__(self):
        return self

    def __exit__(self, err_type, err_value, err_tb):
        self.__del__()

    @staticmethod
    def supported_formats() -> Sequence[str]:
        return "pdf", "png", "svg"


class GraphicsContext:
    """
    A thin wrapper to produce vector graphics using cairo. This class provides a drawing context that we can use to
    draw a figure onto a page.
    """

    def __init__(self,
                 page: GraphicsPage,
                 offset_x: float = 0,
                 offset_y: float = 0,
                 rotation: float = 0):
        """
        A thin wrapper to produce vector graphics using cairo. This class provides a drawing context that we can use to
        draw a figure onto a page.

        :param page:
            The GraphicsPage we are going to draw onto
        :param offset_x:
            The offset of this drawing from (0,0) on the page, metres
        :param offset_y:
            The offset of this drawing from (0,0) on the page, metres
        :param rotation:
            The rotation of this drawing, radians
        """

        assert isinstance(page, GraphicsPage)

        # Record our drawing state
        self.base_line_width: float = line_width_base
        self.base_font_size: float = font_size_base
        self.font_size: Optional[float] = False
        self.font_bold: bool = False
        self.font_italic: bool = False
        self.line_dotted: bool = False

        # Create Cairo context with default settings for requested canvas
        self.context: cairo.Context = cairo.Context(target=page.surface)
        self.context.scale(sx=page.dots_per_metre, sy=page.dots_per_metre)
        self.context.translate(tx=offset_x, ty=offset_y)
        self.context.rotate(radians=rotation * unit_deg)
        self.set_line_width(line_width=1)
        self.set_font_style()
        self.set_font_size(font_size=1)
        self.context.set_fill_rule(fill_rule=cairo.FILL_RULE_EVEN_ODD)

    def __enter__(self):
        return self

    def __exit__(self, err_type, err_value, err_tb):
        pass

    def begin_path(self) -> None:
        """
        Begin a new path.
        """
        self.context.new_path()

    def begin_sub_path(self) -> None:
        """
        Begin a new closed shape within the current path
        """
        self.context.new_sub_path()

    def move_to(self, x: float, y: float) -> None:
        """
        Move

        :param x:
            Position, metres
        :param y:
            Position, metres
        :return:
            None
        """
        self.context.move_to(x=x, y=y)

    def line_to(self, x: float, y: float) -> None:
        """
        Line element

        :param x:
            Position, metres
        :param y:
            Position, metres
        :return:
            None
        """
        self.context.line_to(x=x, y=y)

    def curve_to(self, x0: float, y0: float, x1: float, y1: float, x2: float, y2: float) -> None:
        """
        Bézier curve element

        :param x0:
            First control point, metres
        :param y0:
            First control point, metres
        :param x1:
            Second control point, metres
        :param y1:
            Second control point, metres
        :param x2:
            End point, metres
        :param y2:
            End point, metres
        :return:
            None
        """
        self.context.curve_to(x1=x0, y1=y0, x2=x1, y2=y1, x3=x2, y3=y2)

    def close_path(self) -> None:
        """
        Close the current path.
        """
        self.context.close_path()

    def stroke(self, line_width: Optional[float] = None,
               color: Optional[Sequence[float]] = None, dotted: Optional[bool] = None) -> None:
        """
        Stroke the current path
        """
        if line_width is not None:
            self.set_line_width(line_width=line_width)
        if color is not None:
            self.set_color(color=color)
        if dotted is not None:
            self.set_line_style(dotted=dotted)
        self.context.stroke_preserve()

    def fill(self, color: Optional[Sequence[float]] = None) -> None:
        """
        Fill the current path
        """
        if color is not None:
            self.set_color(color=color)
        self.context.fill_preserve()

    def clip(self) -> None:
        """
        Use the current path as a clipping region.
        """
        self.context.clip()

    def arc(self, centre_x: float, centre_y: float, radius: float, arc_from: float, arc_to: float) -> None:
        """
        Add an arc element to the current path.

        :param centre_x:
            The centre of the arc, metres
        :param centre_y:
            The centre of the arc, metres
        :param radius:
            The radius of the arc, metres
        :param arc_from:
            The angle where the arc is to start, radians
        :param arc_to:
            The angle where the arc is to end, radians
        """
        self.context.arc(xc=centre_x, yc=centre_y, radius=radius, angle1=arc_from, angle2=arc_to)

    def circle(self, centre_x: float, centre_y: float, radius: float) -> None:
        """
        Add an arc element to the current path.

        :param centre_x:
            The centre of the circles, metres
        :param centre_y:
            The centre of the circles, metres
        :param radius:
            The radius of the circles, metres
        """
        self.arc(centre_x=centre_x, centre_y=centre_y, radius=radius, arc_from=0, arc_to=2 * pi)

    def rectangle(self, x0: float, y0: float, x1: float, y1: float) -> None:
        """
        Add a rectangle to the current path.

        :param x0:
            The left side of the box, metres
        :param y0:
            The top side of the box, metres
        :param x1:
            The right side of the box, metres
        :param y1:
            The bottom side of the box, metres
        """
        self.context.rectangle(x=x0, y=y0, width=x1 - x0, height=y1 - y0)

    def set_color(self, color: Sequence[float]) -> None:
        """
        Set the colour used for both stroke and fill operations.

        :param color:
            List of four float values: Red/green/blue/alpha. Each should be a float between 0 and 1.
        :return:
            None
        """
        self.context.set_source_rgba(red=color[0], green=color[1], blue=color[2], alpha=color[3])

    def set_line_style(self, dotted: Optional[bool] = None) -> None:
        """
        Select the stroke style used to stroke lines.

        :param dotted:
            Boolean flag indicating whether lines should be dotted or continuous.
        :return:
            None
        """
        if dotted is not None:
            self.line_dotted = dotted

        if self.line_dotted:
            self.context.set_dash([1.0 * unit_mm])
        else:
            self.context.set_dash([])

    def set_font_size(self, font_size: float) -> None:
        """
        Change the font size used to render text.

        :param font_size:
            Font size, relative to default
        """
        self.font_size = font_size
        self.context.set_font_size(font_size * self.base_font_size)

    def set_font_style(self, italic: Optional[bool] = None, bold: Optional[bool] = None) -> None:
        """
        Sets the font style (i.e. bold or italic) used.

        :param italic:
            Boolean flag, indicating whether text should be italic. None indicates we preserve the existing setting.
        :param bold:
            Boolean flag, indicating whether text should be bold. None indicates we preserve the existing setting.
        """
        if italic is not None:
            self.font_italic = italic
        if bold is not None:
            self.font_bold = bold

        self.context.select_font_face(family="FreeSerif",
                                      slant=cairo.FONT_SLANT_ITALIC if self.font_italic else cairo.FONT_SLANT_NORMAL,
                                      weight=cairo.FONT_WEIGHT_BOLD if self.font_bold else cairo.FONT_SLANT_NORMAL
                                      )

    def set_line_width(self, line_width: float) -> None:
        """
        Sets the line width used to stroke paths.

        :param line_width:
            Line width, relative to the base line-width defined in <constants.py>
        :return:
            None
        """
        self.context.set_line_width(width=line_width * self.base_line_width)

    def text(self, text: str, x: float, y: float,
             h_align: int = 0, v_align: int = 0,
             gap: float = 0, rotation: float = 0) -> None:
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
            The rotation angle of the text, radians
        :return:
            None
        """

        text: str = str(text)
        extent: Dict[str, float] = self.measure_text(text=text)

        # Cairo places top-left of text at specified point. For other alignments, we calculate where this point will be
        offset_x: float = 0
        offset_y: float = 0
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
        self.context.translate(tx=x, ty=y)
        self.context.rotate(radians=rotation)
        self.context.move_to(x=offset_x + gap * h_align, y=offset_y + gap * v_align)
        self.context.show_text(text=text)
        self.context.restore()

    def measure_text(self, text: str) -> Dict[str, float]:
        """
        Measure the dimensions of a string of text, as it would be rendered in the currently-selected font.

        :param text:
            Text string to render
        :return:
            Dictionary of size information about the text string
        """

        # Measure text
        (x, y, width, height, dx, dy) = self.context.text_extents(text=text)

        # Return dimensions
        return {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "dx": dx,
            "dy": dy
        }

    def circular_text(self, text: str, centre_x: float, centre_y: float,
                      radius: float, azimuth: float, spacing: float, size: float) -> None:
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

        self.set_font_size(size)

        # First calculate total length of text
        text_width: float = 0
        for char in text:
            text_width += float(self.measure_text(text=char)['dx']) * 1.1

        # Work out the angular span of the text around the specified circular path
        text_angular_width: float = text_width / radius

        # Work out the azimuth at which we need to start, in order to have centre of text at specified azimuth
        current_azimuth: float = azimuth * unit_deg - spacing * text_angular_width / 2

        # Then render text, one character at a time
        for char in text:
            dimensions: Dict[str, float] = self.measure_text(text=char)
            character_width: float = float(dimensions['dx']) * 1.1
            self.text(text=char,
                      x=centre_x + cos(current_azimuth) * radius,
                      y=centre_y - sin(current_azimuth) * radius,
                      h_align=-1, v_align=-1,
                      rotation=-current_azimuth - 90 * unit_deg
                      )
            current_azimuth += (character_width * spacing) / radius

    def text_wrapped(self, text: str | Sequence, x: float, y: float, width: float,
                     justify: int = 0, line_spacing: float = 1.3,
                     h_align: int = 0, v_align: int = 0, rotation: float = 0) -> None:
        """
        Add a text string to the drawing canvas.

        :param text:
            The string to write
        :param x:
            The horizontal position of the string, metres
        :param y:
            The vertical position of the string, metres
        :param width:
            The maximum allowed length of each line, metres
        :param justify:
            The horizontal justification of the string: -1 left; 0 centred; 1 right
        :param line_spacing:
            The spacing, in line heights, between lines of text
        :param h_align:
            The horizontal alignment of the string: -1 left; 0 centred; 1 right
        :param v_align:
            The vertical alignment of the string: -1 top; 0 centred; 1 bottom
        :param rotation:
            The rotation angle of the text, radians
        """

        if not isinstance(text, (list, tuple)):
            text = [text]

        # Assemble a list of all the lines we are going to display
        line_buffer: List[str] = []

        # Loop through each of the paragraphs of input text, one by one. They are supplied as a list or tuple.
        for paragraph in text:
            line: str = ""
            # Add each word in turn to the current line, until it becomes too long
            for word in paragraph.split():
                line_new = "{} {}".format(line, word).strip()
                line_new_width = self.measure_text(line_new)['width']
                # If the line is too long, start a new line
                if line_new_width > width:
                    line_buffer.append(line)
                    line = word
                # Otherwise, keep adding words to the existing line
                else:
                    line = line_new
            # Add last line of text to buffer
            line_buffer.append(line)

        line_heights: List[float] = [self.font_size * self.base_font_size * line_spacing for line in line_buffer]
        total_height: float = sum(line_heights)

        # Now draw text, line by line
        self.context.save()
        self.context.translate(tx=x, ty=y)
        self.context.rotate(radians=rotation)

        horizontal_anchor: int = justify - h_align
        x_anchor: float = (width / 2) * horizontal_anchor

        if v_align > 0:
            y_anchor: float = 0
        elif v_align == 0:
            y_anchor = -total_height / 2
        else:
            y_anchor = -total_height

        for line_number, line in enumerate(line_buffer):
            self.text(text=line, x=x_anchor, y=y_anchor, h_align=justify, v_align=-1)
            y_anchor += line_heights[line_number]

        self.context.restore()

    def paint_png_image(self, png_filename: str, x_left: float, y_top: float,
                        target_width: float, target_height: float) -> bool:
        """
        Render a PNG image onto the Cairo canvas.

        :param png_filename:
            The filename of the PNG file to render
        :param x_left:
            The X coordinate of the left side of the image on the canvas, metres
        :param y_top:
            The Y coordinate of the top side of the image on the canvas, metres
        :param target_width:
            The intended width of the image, metres
        :param target_height:
            The intended height of the image, metres
        :return:
            Boolean flag indicating whether the image was successfully rendered
        """

        # Save the state of the display context
        self.context.save()
        try:
            # Create a Cairo image surface with the PNG image on it
            image_surface: cairo.ImageSurface = cairo.ImageSurface.create_from_png(png_filename)

            # Measure the PNG image
            img_height: int = image_surface.get_height()
            img_width: int = image_surface.get_width()

            # Calculate proportional scaling to get the image to the desired size
            width_ratio: float = float(target_width) / float(img_width)
            height_ratio: float = float(target_height) / float(img_height)

            # Scale image and add it to the canvas
            self.context.translate(x_left, y_top)
            self.context.scale(width_ratio, height_ratio)
            self.context.set_source_surface(image_surface)

            self.context.paint()
            outcome: bool = True
        except:
            logging.info("Failed to render PNG image")
            outcome = False

        # Make sure that we undo the coordinate transformation, even if the image render fails
        self.context.restore()

        # Return success flag
        return outcome

    def matrix_transformation_set(self, xx: float, yx: float, xy: float, yy: float, x0: float, y0: float,
                                  centre_x: float, centre_y: float) -> None:
        """
        Apply a matrix transformation to the Cairo drawing context.

        x_new = xx * x + xy * y + x0
        y_new = yx * x + yy * y + y0
        """
        self.context.save()
        self.context.translate(tx=centre_x, ty=centre_y)
        self.context.transform(cairo.Matrix(xx=xx, yx=yx, xy=xy, yy=yy, x0=x0, y0=y0))

    def matrix_transformation_restore(self) -> None:
        """
        Undo a matrix transformation to the Cairo drawing context.
        """
        self.context.restore()


class BaseComponent:
    """
    A class wrapping a piece of code used to draw a single component of the model.
    """

    def __init__(self, settings: Optional[dict] = None):
        """
        A class wrapping a piece of code used to draw a single component of the model.

        :param settings:
            Settings used in the rendering of this component
        """

        if settings is None:
            settings = {}
        self.settings: dict = settings

    def render_to_page(self, page: GraphicsPage, offset_x: float = 0, offset_y: float = 0, rotation: float = 0) -> None:
        """
        Render this component onto a Page object.

        :param page:
            The GraphicsPage we are going to draw onto
        :param offset_x:
            The offset of this drawing from (0,0) on the page, metres
        :param offset_y:
            The offset of this drawing from (0,0) on the page, metres
        :param rotation:
            The rotation of this drawing, float
        """

        # Make sure that the page we're going to draw onto is of the correct type
        assert isinstance(page, GraphicsPage)

        # Create a drawing context for drawing onto this page
        with GraphicsContext(page=page, offset_x=offset_x, offset_y=offset_y, rotation=rotation) as context:
            # Render this item
            self.do_rendering(settings=self.settings, context=context)

    def render_to_file(self, filename: Optional[str] = None, img_format: str = "png",
                       dots_per_inch: float = dots_per_inch) -> None:
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
        bounding_box: Dict[str, float] = self.bounding_box(settings=self.settings)

        # If no filename is specified, then individual derived classes should specify a default
        if filename is None:
            filename = self.default_filename()

        # Create a graphics page large enough to hold this item
        with GraphicsPage(img_format=img_format, output=filename,
                          width=bounding_box['x_max'] - bounding_box['x_min'],
                          height=bounding_box['y_max'] - bounding_box['y_min'],
                          dots_per_inch=dots_per_inch
                          ) as page:
            # Render the item
            self.render_to_page(page=page,
                                offset_x=-bounding_box['x_min'],
                                offset_y=-bounding_box['y_min'])

    def render_all_formats(self, filename: Optional[str] = None, dots_per_inch: float = dots_per_inch) -> None:
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

    def bounding_box(self, settings: dict) -> Dict[str, float]:
        """
        This method is required to report the bounding box of the canvas area used by this item.

        :param settings:
            A dictionary of settings required by the renderer.
        :return:
            Dictionary with the elements 'x_min', 'x_max', 'y_min and 'y_max' set to the canvas area required.
        """
        raise NotImplementedError("Derived classes of type <BaseComponent> must implement a method <bounding_box> "
                                  "which reports the area of canvas they require.")

    def default_filename(self) -> str:
        """
        This method is required to report a default filename to use for this item, without file type suffix.

        :return:
            string
        """
        raise NotImplementedError("Derived classes of type <BaseComponent> must implement a method "
                                  "<default_filename> which report a default filename to use for this item, without "
                                  "file type suffix.")

    def do_rendering(self, settings: dict, context: GraphicsContext) -> None:
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

    def __init__(self, components: Sequence[BaseComponent], settings: Optional[dict] = None):
        self.components: Sequence[BaseComponent] = components
        super(CompositeComponent, self).__init__(settings=settings)

    def default_filename(self) -> str:
        return "composite_page"

    def bounding_box(self, settings: dict) -> Dict[str, float]:
        """
        Work out overall bounding box of all items when constituent components are overlaid.

        :param settings:
            A dictionary of settings required by the renderer.
        """

        bounding_boxes: Sequence[Dict[str, float]] = [item.bounding_box(settings=item.settings)
                                                      for item in self.components]

        return {
            'x_min': min([item['x_min'] for item in bounding_boxes]),
            'x_max': max([item['x_max'] for item in bounding_boxes]),
            'y_min': min([item['y_min'] for item in bounding_boxes]),
            'y_max': max([item['y_max'] for item in bounding_boxes]),
        }

    def do_rendering(self, settings: dict, context: GraphicsContext) -> None:
        """
        Render each of the subcomponents we are overlaying in turn.

        :param settings:
            A dictionary of settings required by the renderer.
        :param context:
            A GraphicsContext object to use for drawing
        :return:
            None
        """

        for item in self.components:
            item.do_rendering(settings=settings, context=context)
