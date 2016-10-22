# -*- coding: utf-8 -*-
"""Controller
A view can be any output representation of information, such as a chart or a diagram. `<Wikipedia>
<https://en.wikipedia.org/wiki/Model–view–controller>`_

Here is a view example:

.. testcode::

    from dp_tornado.engine.controller import Controller

    class FooBarController(Controller):
        def get(self):
            self.render('index.html')
"""

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
        if engine.helper.misc.system.py_version <= 2:
            if kwargs:
                return engine.helper.string.cast.string(controller.parent.render_string(template_name, **kwargs))
            else:
                return engine.helper.string.cast.string(controller.parent.render_string(template_name))
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
