# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.10.23
#


from .singleton import Singleton


class View(object, metaclass=Singleton):
    @staticmethod
    def render(controller, template_name, kwargs=None):
        if kwargs:
            controller.parent.render(template_name, **kwargs)
        else:
            controller.parent.render(template_name)

    @staticmethod
    def render_string(controller, template_name, kwargs=None):
        if kwargs:
            return str(controller.parent.render_string(template_name, **kwargs), 'UTF-8')
        else:
            return str(controller.parent.render_string(template_name), 'UTF-8')

    @staticmethod
    def write(controller, chunk):
        controller.parent.write(chunk)

    @staticmethod
    def finish(controller, chunk=None):
        controller.parent.finish(chunk)