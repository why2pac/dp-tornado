# -*- coding: utf-8 -*-


import os

from urllib2 import urlopen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps

from dp_tornado.engine.helper import Helper as dpHelper


class ResizeHelper(dpHelper):
    def rounded_mask(self, size, radius, factor=2):
        width, height = size
        radius = min(radius, *size)

        mask = Image.new("L", (width * factor, height * factor))
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, radius * factor, radius * factor), fill='#FFFFFF')

        flip = mask.transpose(Image.FLIP_LEFT_RIGHT)
        mask.paste(flip, (0, 0), flip)
        mask_draw.rectangle((radius * factor / 2, 0, (width - (radius / 2)) * factor, radius * factor), fill='#FFFFFF')
        flip = mask.transpose(Image.FLIP_TOP_BOTTOM)
        mask.paste(flip, (0, 0), flip)
        mask_draw.rectangle((0, radius * factor / 2, width * factor, (height - (radius / 2)) * factor), fill='#FFFFFF')
        mask = mask.resize((width, height), Image.ANTIALIAS)

        return mask

    def resizing(self, filename, size, **kwargs):
        mode = kwargs['mode'] if 'mode' in kwargs else None
        scale = int(kwargs['scale']) if 'scale' in kwargs else 1
        edge_crop = kwargs['edge_crop'] if 'edge_crop' in kwargs else None
        border = int(kwargs['border']) if 'border' in kwargs else 0
        border_color = kwargs['border_color'] if 'border_color' in kwargs else '#000000'
        limit = True if 'limit' in kwargs and kwargs['limit'] else False
        background = kwargs['background'] if 'background' in kwargs else None
        colorize = kwargs['colorize'] if 'colorize' in kwargs else None
        radius = int(kwargs['radius'] or 0) if 'radius' in kwargs else None
        save = kwargs['save'] if 'save' in kwargs else None
        fmt = kwargs['fmt'] if 'fmt' in kwargs else None

        if not os.path.isfile(filename):
            f = urlopen(filename)
            img = Image.open(f)
        else:
            img = Image.open(filename)

        if not img:
            raise Exception('The specified image is invalid.')

        # Edge Cropping
        if edge_crop:
            e_top = 0
            e_left = 0
            e_right = 0
            e_bottom = 0

            if self.helper.system.py_version <= 2:
                types_str = (basestring, )
                types_num = (int, long)
            else:
                types_str = (str, )
                types_num = (int, )

            if isinstance(edge_crop, types_str):
                edge_crop = edge_crop.split(',')

                for i in range(len(edge_crop)):
                    edge_crop[i] = int(edge_crop[i])

            if isinstance(edge_crop, types_num):
                e_top = e_left = e_right = e_bottom = edge_crop

            elif isinstance(edge_crop, (tuple, list)):
                if len(edge_crop) == 1:
                    e_top = e_left = e_right = e_bottom = edge_crop[0]

                elif len(edge_crop) == 2:
                    e_top = e_bottom = edge_crop[0]
                    e_left = e_right = edge_crop[1]

                elif len(edge_crop) == 4:
                    e_top = edge_crop[0]
                    e_right = edge_crop[1]
                    e_bottom = edge_crop[2]
                    e_left = edge_crop[3]

            img = img.crop((e_left, e_top, img.size[0] - e_right, img.size[1] - e_bottom))

        ext = (fmt or os.path.splitext(filename)[1][1:]).lower()
        width_new, height_new = size
        width_origin, height_origin = img.size

        if scale > 1:
            if limit:
                scale_max_width = float(width_origin) / float(width_new)
                scale_max_height = float(height_origin) / float(height_new)

                scale_max = min(scale, scale_max_width, scale_max_height)
            else:
                scale_max = scale

            if scale_max > 1:
                width_new = int(width_new * scale_max)
                height_new = int(height_new * scale_max)

        if not width_new:
            width_new = width_origin * height_new / height_origin
            mode = self.helper.image.resize.mode.resize

        if not height_new:
            height_new = height_origin * width_new / width_origin
            mode = self.helper.image.resize.mode.resize

        if border:
            width_new -= border * 2
            height_new -= border * 2

        if not mode:
            mode = self.helper.image.resize.mode.resize

        if mode not in self.helper.image.resize.mode.modes:
            raise Exception('The specified mode is not supported.')

        # Image Resizing
        if mode == self.helper.image.resize.mode.center:
            width_calc = width_new
            height_calc = height_origin * width_calc / width_origin

            if height_calc > height_new:
                height_calc = height_new
                width_calc = width_origin * height_calc / height_origin

            img = img.resize((width_calc, height_calc), Image.ANTIALIAS)

            if radius:
                fmt = 'PNG'
                img = img.convert('RGBA')
                img.putalpha(self.rounded_mask(img.size, radius))
                radius = None

            img = ImageOps.expand(
                img, border=((width_new - width_calc) / 2, (height_new - height_calc) / 2), fill=background)

        elif mode == self.helper.image.resize.mode.fill:
            ratio_origin = float(width_origin) / float(height_origin)
            ratio_new = float(width_new) / float(height_new)

            if ratio_origin > ratio_new:
                tw = int(round(height_new * ratio_origin))
                img = img.resize((tw, height_new), Image.ANTIALIAS)
                left = int(round((tw - width_new) / 2.0))
                img = img.crop((left, 0, left + width_new, height_new))

            elif ratio_origin < ratio_new:
                th = int(round(width_new / ratio_origin))
                img = img.resize((width_new, th), Image.ANTIALIAS)
                top = int(round((th - height_new) / 2.0))
                img = img.crop((0, top, width_new, top+height_new))

            else:
                img = img.resize((width_new, height_new), Image.ANTIALIAS)

        elif mode == self.helper.image.resize.mode.resize:
            if width_new > width_origin or height_new > height_origin:
                width_new = width_origin
                height_new = height_origin

            img = img.resize((width_new, height_new), Image.ANTIALIAS)

        # Colorizing
        if colorize:
            img = img.convert('RGBA')
            r, g, b, a = img.split()
            gray = ImageOps.grayscale(img)
            result = ImageOps.colorize(gray, colorize, (255, 255, 255, 0))
            result.putalpha(a)
            img = result

        # PNG : 1, L, P, RGB, RGBA
        # GIF : L, P
        # JPEG : L, RGB, CMYK

        # Invalid format specified
        if not fmt and ext in ('jpg', 'jpeg') and img.mode == 'P':  # JPEG not supported P mode
            img = img.convert('RGBA')

        # Border without radius
        if border and not radius:
            if img.mode == 'P':
                img = img.convert('RGBA')

            img = ImageOps.expand(img, border=(border, border), fill=border_color)

        # Add rounded corner
        if radius:
            fmt = 'PNG'
            img = img.convert('RGBA')
            img.putalpha(self.rounded_mask(img.size, min(radius, *img.size)))

            # Border with radius
            if border:
                img_o = img

                bordered_size = (img.size[0] + (border * 2), img.size[1] + (border * 2))
                img = Image.new('RGBA', bordered_size, border_color)
                img.putalpha(self.rounded_mask(bordered_size, min(radius, *bordered_size)))
                img.paste(img_o, (border, border), img_o)

        if save:
            img.save(save, format=fmt, quality=100)

        return img
