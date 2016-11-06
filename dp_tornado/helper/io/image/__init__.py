# -*- coding: utf-8 -*-


import tempfile

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

from dp_tornado.engine.helper import Helper as dpHelper


class ImageHelper(dpHelper):
    def compare(self, i1, i2, error=0):
        i1 = self.load(i1)
        i2 = self.load(i2)

        if not i1 or not i2:
            return None

        s1 = i1.size
        s2 = i2.size

        if s1[0] != s2[0] or s2[1] != s2[1]:
            print('size ne,', s1, s2)
            return False

        i1 = i1.load()
        i2 = i2.load()

        for i in range(s1[0]):
            for j in range(s1[1]):
                if i1[i, j] != i2[i, j]:
                    if error:
                        for k in range(len(i1[i, j])):
                            if abs(i1[i, j][k] - i2[i, j][k]) > error:
                                print('pixel ne,', i1[i, j], i2[i, j], abs(i1[i, j][k] - i2[i, j][k]), error)
                                return False
                    else:
                        return False

        return True

    def load(self, src):
        tmp = None

        try:
            if isinstance(src, Image.Image):
                return src

            elif self.helper.web.url.validate(src):
                code, res = self.helper.web.http.get.raw(src)

                if code != 200:
                    return False

                tmp = tempfile.NamedTemporaryFile(delete=False)
                tmp.write(res)
                tmp.close()

                tmp = tmp.name

            else:
                tmp = None

            img = Image.open(tmp if tmp else src)

            if not img:
                raise Exception('The specified image is invalid.')

            return img

        except Exception as e:
            self.logging.exception(e)

            return False

        finally:
            if tmp:
                self.helper.io.file.remove(tmp)

    def execute(self, src, fn, **kwargs):
        img = self.load(src)

        if not img:
            return False

        try:
            return fn(img, **kwargs)

        except Exception as e:
            self.logging.exception(e)

            return False

    def size(self, src, **o_kwargs):
        def fn(img, **kwargs):
            if not img:
                return -1, -1

            return img.width, img.height

        return self.execute(src, fn, **o_kwargs)

    def crop(self, src, **o_kwargs):
        def fn(img, **kwargs):
            crop = kwargs['crop'] if 'crop' in kwargs else None

            if not crop:
                return img

            e_top = 0
            e_left = 0
            e_right = 0
            e_bottom = 0

            if self.helper.misc.type.check.string(crop):
                crop = crop.split(',')
                crop = [int(e.strip()) for e in crop]

            if self.helper.misc.type.check.numeric(crop):
                e_top = e_left = e_right = e_bottom = crop

            elif isinstance(crop, (tuple, list)):
                if len(crop) == 1:
                    e_top = e_left = e_right = e_bottom = crop[0]

                elif len(crop) == 2:
                    e_top = e_bottom = crop[0]
                    e_left = e_right = crop[1]

                elif len(crop) == 4:
                    e_top = crop[0]
                    e_right = crop[1]
                    e_bottom = crop[2]
                    e_left = crop[3]

            img = img.crop((e_left, e_top, img.size[0] - e_right, img.size[1] - e_bottom))

            return img

        return self.execute(src, fn, **o_kwargs)

    def border(self, src, **o_kwargs):
        def fn(img, **kwargs):
            border = int(kwargs['border']) if 'border' in kwargs else 0
            border_color = kwargs['border_color'] if 'border_color' in kwargs else '#000000'

            if not border:
                return img

            if '_org' in kwargs and 'radius' in kwargs and kwargs['radius']:
                return img

            if img.mode == 'P':
                img = img.convert('RGBA')

            img = ImageOps.expand(img, border=(border, border), fill=border_color)

            return img

        return self.execute(src, fn, **o_kwargs)

    def radius(self, src, **o_kwargs):
        def fn(img, **kwargs):
            radius = int(kwargs['radius'] or 0) if 'radius' in kwargs else None
            border = int(kwargs['border']) if 'border' in kwargs else 0
            border_color = kwargs['border_color'] if 'border_color' in kwargs else '#000000'

            if not radius:
                return img
            elif '__radius_processed__' in img.__dict__:
                return img

            img = img.convert('RGBA')
            img.putalpha(self._rounded_mask(img.size, min(radius, *img.size)))

            # Border with radius
            if border:
                img_o = img
                bordered_size = (img.size[0] + (border * 2), img.size[1] + (border * 2))
                img = Image.new('RGBA', bordered_size, border_color)
                img.putalpha(self._rounded_mask(bordered_size, min(radius, *bordered_size)))
                img.paste(img_o, (border, border), img_o)

            img.__dict__['__radius_processed__'] = True

            return img

        return self.execute(src, fn, **o_kwargs)

    def colorize(self, src, **o_kwargs):
        def fn(img, **kwargs):
            colorize = kwargs['colorize'] if 'colorize' in kwargs else None

            if not colorize:
                return img

            img = img.convert('RGBA')
            r, g, b, a = img.split()
            gray = ImageOps.grayscale(img)
            result = ImageOps.colorize(gray, colorize, (255, 255, 255, 0))
            result.putalpha(a)
            img = result

            return img

        return self.execute(src, fn, **o_kwargs)

    def resize(self, src, **o_kwargs):
        def fn(img, **kwargs):
            size = kwargs['size'] if 'size' in kwargs else None
            mode = kwargs['mode'] if 'mode' in kwargs else None
            scale = int(kwargs['scale']) if 'scale' in kwargs else 1
            limit = True if 'limit' in kwargs and kwargs['limit'] else False
            background = kwargs['background'] if 'background' in kwargs else None
            border = int(kwargs['border']) if 'border' in kwargs else 0

            if not size:
                return img

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
                mode = self.helper.io.image.mode.resize

            if not height_new:
                height_new = height_origin * width_new / width_origin
                mode = self.helper.io.image.mode.resize

            if border:
                width_new -= border * 2
                height_new -= border * 2

            if not mode:
                mode = self.helper.io.image.mode.resize

            if mode not in self.helper.io.image.mode.modes:
                raise Exception('The specified mode is not supported.')

            # Image Resizing
            if mode == self.helper.io.image.mode.center:
                width_calc = width_new
                height_calc = height_origin * width_calc / width_origin

                if height_calc > height_new:
                    height_calc = height_new
                    width_calc = width_origin * height_calc / height_origin

                img = img.resize((int(width_calc), int(height_calc)), Image.ANTIALIAS)
                img = self.radius(img, **kwargs)

                img = ImageOps.expand(
                    img, border=(int((width_new - width_calc) / 2), int((height_new - height_calc) / 2)), fill=background)

                radius = int(kwargs['radius'] or 0) if 'radius' in kwargs else None

                if radius:
                    img_empty = Image.new('RGB', (width_new, height_new), background)
                    img_empty.paste(img, (0, 0), img)
                    img = img_empty

                img.__dict__['__radius_processed__'] = True

            elif mode == self.helper.io.image.mode.fill:
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
                    img = img.crop((0, top, width_new, top + height_new))

                else:
                    img = img.resize((width_new, height_new), Image.ANTIALIAS)

            elif mode == self.helper.io.image.mode.resize:
                if width_new > width_origin or height_new > height_origin:
                    width_new = width_origin
                    height_new = height_origin

                img = img.resize((width_new, height_new), Image.ANTIALIAS)

            return img

        return self.execute(src, fn, **o_kwargs)

    def save(self, src, **o_kwargs):
        def fn(img, **kwargs):
            ext = kwargs['format'] if 'format' in kwargs else None
            dest = kwargs['dest'] if 'dest' in kwargs else None

            if not dest:
                return None

            if not ext and self.helper.misc.type.check.string(dest):
                ext = self.helper.io.path.ext(dest, dot='').lower()

            if not ext and self.helper.misc.type.check.string(src):
                ext = self.helper.io.path.ext(src, dot='').lower()

            if not ext and '_org' in kwargs and kwargs['_org'] and self.helper.misc.type.check.string(kwargs['_org']):
                ext = self.helper.io.path.ext(kwargs['_org'], dot='').lower()

            if dest == 's3':
                # TODO
                return False

            # PNG : 1, L, P, RGB, RGBA
            # GIF : L, P
            # JPEG : L, RGB, CMYK

            # Invalid format specified
            if ext in ('jpg', 'jpeg') and img.mode == 'P':  # JPEG does not support P mode
                img = img.convert('RGBA')

            img.save(dest, format=ext, quality=100)

            return True

        return self.execute(src, fn, **o_kwargs)

    def manipulate(self, src, **kwargs):
        kwargs['_org'] = src

        try:
            img = self.load(src)

            # Crop
            img = self.crop(img, **kwargs)

            if not img:
                return False

            # Resize
            img = self.resize(img, **kwargs)

            if not img:
                return False

            # Radius
            img = self.radius(img, **kwargs)

            if not img:
                return False

            # Border
            img = self.border(img, **kwargs)

            if not img:
                return False

            # Colorize
            img = self.colorize(img, **kwargs)

            if not img:
                return False

            # Save
            saved = self.save(img, **kwargs)

            if saved is None:
                return img
            elif saved is False:
                return False

            return True

        except Exception as e:
            self.logging.exception(e)

            return False

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
