# -*- coding: utf-8 -*-


from .singleton import Singleton as dpSingleton
from .engine import Engine as dpEngine

engine = dpEngine()


class View(dpSingleton):
    @staticmethod
    def render(controller, template_name, kwargs=None):
        if kwargs:
            controller.parent.render(template_name, **kwargs)
        else:
            controller.parent.render(template_name)

    @staticmethod
    def render_string(controller, template_name, kwargs=None):
        if engine.helper.system.py_version <= 2:
            if kwargs:
                return engine.helper.string.to_str(controller.parent.render_string(template_name, **kwargs))
            else:
                return engine.helper.string.to_str(controller.parent.render_string(template_name))
        else:
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