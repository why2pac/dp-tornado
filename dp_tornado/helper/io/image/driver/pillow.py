# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    from PIL import ImageDraw
except ImportError:
    ImageDraw = None

try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None


class PillowHelper(dpHelper):
    @property
    def Image(self):
        return Image.Image

    def load(self, src):
        return Image.open(src)

    def size(self, src):
        return src.width, src.height

    def crop(self, img, left, top, right, bottom):
        return img.crop((left, top, right, bottom))

    def resize(self, img, width, height, kwargs=None):
        if kwargs is None:
            img = img.resize((width, height), Image.ANTIALIAS)
        else:
            background = kwargs['background'] if 'background' in kwargs else None
            mode = kwargs['mode'] if 'mode' in kwargs else None

            if mode == self.helper.io.image.mode.center:
                width_new, height_new = (width, height)
                width_origin, height_origin = img.size

                width_calc = width_new
                height_calc = height_origin * width_calc / width_origin

                if height_calc > height_new:
                    height_calc = height_new
                    width_calc = width_origin * height_calc / height_origin

                img = img.resize((int(width_calc), int(height_calc)), Image.ANTIALIAS)
                img = self.helper.io.image.radius(img, **kwargs)

                img = ImageOps.expand(
                    img, border=(int((width - width_calc) / 2), int((height_new - height_calc) / 2)), fill=background)

                radius = int(kwargs['radius'] or 0) if 'radius' in kwargs else None

                if radius:
                    img_empty = Image.new('RGB', (width, height_new), background)
                    img_empty.paste(img, (0, 0), img)
                    img = img_empty

                img.__dict__['__radius_processed__'] = True

        return img

    def border(self, img, border, border_color):
        if img.mode == 'P':
            img = img.convert('RGBA')

        img = ImageOps.expand(img, border=(border, border), fill=border_color)

        return img

    def radius(self, img, radius, border, border_color):
        img = img.convert('RGBA')
        img.putalpha(self._rounded_mask(img.size, min(radius, *img.size)))

        # Border with radius
        if border:
            img_o = img
            bordered_size = (img.size[0] + (border * 2), img.size[1] + (border * 2))
            img = Image.new('RGBA', bordered_size, border_color)
            img.putalpha(self._rounded_mask(bordered_size, min(radius, *bordered_size)))
            img.paste(img_o, (border, border), img_o)

        return img

    def colorize(self, img, colorize):
        img = img.convert('RGBA')
        r, g, b, a = img.split()
        gray = ImageOps.grayscale(img)
        result = ImageOps.colorize(gray, colorize, (255, 255, 255, 0))
        result.putalpha(a)
        img = result

        return img

    def save(self, img, ext, dest, kwargs):
        # PNG : 1, L, P, RGB, RGBA
        # GIF : L, P
        # JPEG : L, RGB, CMYK

        # Invalid format specified
        if ext.lower() in ('jpg', 'jpeg') and img.mode == 'P':  # JPEG does not support P mode
            img = img.convert('RGBA')

        if ext.lower() == 'jpg':
            ext = 'jpeg'

        args = {
            'format': ext,
            'quality': 100
        }

        if self._animatable(img, kwargs):
            transparency = img.info['transparency'] if 'transparency' in img.info else None
            background = img.info['background'] if 'background' in img.info else None

            # PILLOW Issue, #1592 (github)

            seqs = []

            for i, im in self._iter_seqs(img, kwargs):
                im = im.convert('RGBA')

                if transparency is not None:
                    im.info['transparency'] = transparency
                if background is not None:
                    im.info['background'] = background

                seqs.append(im)

            img = seqs[0]
            seqs.remove(img)

            if transparency is not None:
                args['transparency'] = transparency
            if background is not None:
                args['background'] = background

            args['append_images'] = seqs
            args['save_all'] = True
            args['format'] = 'GIF'

        img.save(dest, **args)

        return True

    def iter_seqs(self, img, kwargs):
        if '__frames__' in img.__dict__ and img.__dict__['__frames__']:
            yield 0, img

            for i in range(1, min(len(img.__dict__['__frames__']), self._iterable_frames(kwargs)) - 1):
                yield i, img.__dict__['__frames__'][i]

        elif not self._animatable(img, kwargs):
            yield 0, img

        else:
            for i in range(min(img.n_frames, self._iterable_frames(kwargs))):
                img.seek(i)
                yield i, img

    def _iterable_frames(self, kwargs):
        if kwargs['frame'] is True or not self.helper.misc.type.check.numeric(kwargs['frame']):
            return 10**7
        else:
            return kwargs['frame']

    def _animatable(self, img, kwargs):
        if '__frames__' in img.__dict__ and img.__dict__['__frames__']:
            return True

        if 'frame' not in kwargs or not kwargs['frame']:
            return False

        if not img:
            return False

        if not img.format or img.format.upper() != 'GIF':
            return False

        if not img.mode or img.mode.upper() != 'P':
            return False

        if not getattr(img, 'n_frames', None) or img.n_frames <= 1:
            return False

        return True

    def _rounded_mask(self, size, radius, factor=2):
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

