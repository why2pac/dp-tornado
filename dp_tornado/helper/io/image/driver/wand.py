# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

try:
    from wand.image import Image
except ImportError:
    Image = None


class WandHelper(dpHelper):
    @property
    def Image(self):
        return Image

    def load(self, src):
        return Image(filename=src)

    def size(self, src):
        return src.width, src.height

    def crop(self, img, left, top, right, bottom):
        img.crop(left, top, right, bottom)
        return img

    def resize(self, img, width, height, kwargs=None):
        if kwargs is None:
            img.resize(width, height)
        else:
            raise Exception('Not implemented method.')

        return img

    def border(self, img, border, border_color):
        raise Exception('Not implemented method.')

    def radius(self, img, radius, border, border_color):
        raise Exception('Not implemented method.')

    def colorize(self, img, colorize):
        raise Exception('Not implemented method.')

    def save(self, img, ext, dest, kwargs):
        if ext.lower() == 'jpg':
            ext = 'jpeg'

        img.format = ext
        img.save(filename=dest)

        return True

    def iter_seqs(self, img, kwargs):
        yield 0, img
