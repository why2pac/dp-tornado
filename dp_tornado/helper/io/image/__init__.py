# -*- coding: utf-8 -*-


import tempfile

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

    def _driver(self, options=None, **kwargs):
        if not options and kwargs:
            options = kwargs

        if options and 'driver' in options and options['driver'] == 'wand':
            return self.helper.io.image.driver.wand

        return self.helper.io.image.driver.pillow

    def load(self, src, options=None, **kwargs):
        if not options and kwargs:
            options = kwargs

        tmp = None
        drivers = []

        pillow_image = self.helper.io.image.driver.pillow.Image
        wand_image = self.helper.io.image.driver.wand.Image

        if pillow_image:
            drivers.append(pillow_image)

        if wand_image:
            drivers.append(wand_image)

        try:
            if isinstance(src, tuple(drivers)):
                return src

            elif self.helper.web.url.validate(src):
                code, res = self.helper.web.http.get.raw(src)

                if code != 200:
                    raise Exception('The specified image url is invalid.')

                tmp = tempfile.NamedTemporaryFile(delete=False)
                tmp.write(res)
                tmp.close()

                tmp = tmp.name

            else:
                tmp = None

            if not tmp and not src:
                raise Exception('The specified image is invalid.')

            img = self._driver(options=options).load(tmp if tmp else src)

            if not img:
                raise Exception('The specified image is invalid.')

            return img

        except Exception as e:
            self.logging.exception(e)

            return False

        finally:
            if tmp:
                self.helper.io.file.remove(tmp)

    def execute(self, src, fn, options=None, **kwargs):
        if not options and kwargs:
            options = kwargs

        img = self.load(src, options=options)

        if not img:
            return False

        try:
            return fn(img, options)

        except Exception as e:
            self.logging.exception(e)

            return False

    def size(self, src, options=None, **o_kwargs):
        if not options and o_kwargs:
            options = o_kwargs

        def fn(img, kwargs):
            if not img:
                return -1, -1

            return img.width, img.height

        return self.execute(src, fn, options=options)

    def crop(self, src, options=None, **o_kwargs):
        if not options and o_kwargs:
            options = o_kwargs

        def fn(img, kwargs):
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

            img = self._driver(options=kwargs).crop(img, e_left, e_top, img.size[0] - e_right, img.size[1] - e_bottom)

            return img

        return self.execute(src, fn, options=options)

    def border(self, src, options=None, **o_kwargs):
        if not options and o_kwargs:
            options = o_kwargs

        def fn(img, kwargs):
            border = int(kwargs['border']) if 'border' in kwargs else 0
            border_color = kwargs['border_color'] if 'border_color' in kwargs else '#000000'

            if not border:
                return img

            if '_org' in kwargs and 'radius' in kwargs and kwargs['radius']:
                return img

            img = self._driver(options=kwargs).border(img, border, border_color)

            return img

        return self.execute(src, fn, options=options)

    def radius(self, src, options=None, **o_kwargs):
        if not options and o_kwargs:
            options = o_kwargs

        def fn(img, kwargs):
            radius = int(kwargs['radius'] or 0) if 'radius' in kwargs else None
            border = int(kwargs['border']) if 'border' in kwargs else 0
            border_color = kwargs['border_color'] if 'border_color' in kwargs else '#000000'

            if not radius:
                return img
            elif '__radius_processed__' in img.__dict__:
                return img

            img = self._driver(options=kwargs).radius(img, radius, border, border_color)
            img.__dict__['__radius_processed__'] = True

            return img

        return self.execute(src, fn, options=options)

    def colorize(self, src, options=None, **o_kwargs):
        if not options and o_kwargs:
            options = o_kwargs

        def fn(img, kwargs):
            colorize = kwargs['colorize'] if 'colorize' in kwargs else None

            if not colorize:
                return img

            img = self._driver(options=kwargs).colorize(img, colorize)

            return img

        return self.execute(src, fn, options=options)

    def resize(self, src, options=None, **o_kwargs):
        if not options and o_kwargs:
            options = o_kwargs

        def fn(img, kwargs):
            size = kwargs['size'] if 'size' in kwargs else None
            mode = kwargs['mode'] if 'mode' in kwargs else None
            scale = int(kwargs['scale']) if 'scale' in kwargs else 1
            limit = True if 'limit' in kwargs and kwargs['limit'] else False
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

            seqs = []

            for i, im in self._driver(options=kwargs).iter_seqs(img, kwargs):
                # Image Resizing
                if mode == self.helper.io.image.mode.center:
                    im = self._driver(options=kwargs).resize(im, width_new, height_new, kwargs)

                elif mode == self.helper.io.image.mode.fill:
                    ratio_origin = float(width_origin) / float(height_origin)
                    ratio_new = float(width_new) / float(height_new)

                    if ratio_origin > ratio_new:
                        tw = int(round(height_new * ratio_origin))
                        im = self._driver(options=kwargs).resize(im, tw, height_new)
                        left = int(round((tw - width_new) / 2.0))
                        im = self._driver(options=kwargs).crop(im, left, 0, left + width_new, height_new)

                    elif ratio_origin < ratio_new:
                        th = int(round(width_new / ratio_origin))
                        im = self._driver(options=kwargs).resize(im, width_new, th)
                        top = int(round((th - height_new) / 2.0))
                        im = self._driver(options=kwargs).crop(im, 0, top, width_new, top + height_new)

                    else:
                        im = self._driver(options=kwargs).resize(im, width_new, height_new)

                elif mode == self.helper.io.image.mode.resize:
                    if width_new > width_origin or height_new > height_origin:
                        width_new = width_origin
                        height_new = height_origin

                    im = self._driver(options=kwargs).resize(im, width_new, height_new)

                seqs.append(im)

            img = seqs[0]
            seqs.remove(img)
            img.__dict__['__frames__'] = seqs

            return img

        return self.execute(src, fn, options=options)

    def save(self, src, options=None, **o_kwargs):
        if not options and o_kwargs:
            options = o_kwargs

        def fn(img, kwargs):
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

            if not self._driver(options=kwargs).save(img, ext, dest, kwargs):
                return False

            return True

        return self.execute(src, fn, options=options)

    def manipulate(self, src, options=None, **kwargs):
        if not options and kwargs:
            options = kwargs

        options['_org'] = src

        try:
            img = self.load(src, options=options)

            # Crop
            img = self.crop(img, options=options)

            if not img:
                return False

            # Resize
            img = self.resize(img, options=options)

            if not img:
                return False

            # Radius
            img = self.radius(img, options=options)

            if not img:
                return False

            # Border
            img = self.border(img, options=options)

            if not img:
                return False

            # Colorize
            img = self.colorize(img, options=options)

            if not img:
                return False

            # Save
            saved = self.save(img, options=options)

            if saved is None:
                return img
            elif saved is False:
                return False

            return True

        except Exception as e:
            self.logging.exception(e)

            return False
