# -*- coding: utf-8 -*-
"""A view can be any output representation of information, such as a chart or a diagram. `<Wikipedia>
<https://en.wikipedia.org/wiki/Model–view–controller>`_

Here is a view example:

.. testcode::

    from dp_tornado.engine.controller import Controller

    class FooBarController(Controller):
        def get(self):
            self.render('index.html')
"""

from dp_tornado.engine.singleton import Singleton as dpSingleton
from dp_tornado.engine.plugin.static import StaticURL
from dp_tornado.engine.plugin.pagination import Pagination
from dp_tornado.engine.plugin import ui_methods
from dp_tornado.engine.engine import Engine as dpEngine

from tornado import template

import os

engine = dpEngine()


class Dummy(object):
    pass


class View(dpSingleton):
    @staticmethod
    def _ui_modules():
        if getattr(View, '__ui_modules', None) is not None:
            return getattr(View, '__ui_modules')

        o = {
            'Static': StaticURL,
            'Pagination': Pagination
        }

        setattr(View, '__ui_modules', o)

        return o

    @staticmethod
    def _ui_methods():
        if getattr(View, '__ui_methods', None) is not None:
            return getattr(View, '__ui_methods')

        o = {}

        for e in dir(ui_methods):
            if not e.startswith("_") and e[0].lower() == e[0]:
                o[e] = getattr(ui_methods, e)

        setattr(View, '__ui_methods', o)

        return o

    @staticmethod
    def _ui_namespaces(controller):
        o = {
            'c': lambda *args, **kwargs: controller,
            '_tt_modules': Dummy()
        }

        for k, v in View._ui_modules().items():
            setattr(o['_tt_modules'], k, v(controller).render)

        for k, v in View._ui_methods().items():
            o[k] = View._ui_method(controller, v)

        return o

    @staticmethod
    def _ui_method(controller, method):
        return lambda *args, **kwargs: method(controller, *args, **kwargs)

    @staticmethod
    def _loader():
        if getattr(View, '__loader', None) is not None:
            return getattr(View, '__loader')

        o = template.Loader(os.path.join(engine.ini.server.application_path, 'view'))
        setattr(View, '__loader', o)

        return o

    @staticmethod
    def render(controller, template_name, kwargs=None):
        controller.finish(View.render_string(template_name, kwargs, encode=False))

    @staticmethod
    def render_string(controller, template_name, kwargs=None, encode=True):
        l = View._loader()

        if controller.ini.server.debug:
            l.reset()

        t = l.load(template_name)
        n = View._ui_namespaces(controller)
        n.update(kwargs if kwargs else {})
        t = t.generate(**n)

        if encode is True:
            if engine.helper.misc.system.py_version <= 2:
                return engine.helper.string.cast.string(t)
            else:
                return str(t, 'UTF-8')

        return t

    @staticmethod
    def write(controller, chunk):
        controller.parent.write(chunk)

    @staticmethod
    def finish(controller, chunk=None):
        controller.parent.finish(chunk)
