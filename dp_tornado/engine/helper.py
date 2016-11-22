# -*- coding: utf-8 -*-
"""Here is a `foo_bar` helper example:

.. testcode::

    from dp_tornado.engine.helper import Helper as dpHelper

    class FooHelper(dpHelper):
        def func1(self):
            \"""
            assert self.helper.foo.func1(10, 20) == None
            \"""
            return None

        def func2(self, a):
            \"""
            assert self.helper.foo.func2(10) == 10
            \"""
            return a

        def func3(self, a, b):
            \"""
            assert self.helper.foo.func3(10, 20) == 30
            \"""
            return a + b


File/Class Invoke rules
-----------------------
* */helper/__init__.py*, **DO NOT IMPLEMENT ANY CODE IN THIS FILE**
* */helper/blog/__init__.py*, ``BlogHelper`` > **helper.blog**
* */helper/blog/admin/__init__.py*, ``AdminHelper`` > **helper.blog.admin**
* */helper/blog/post.py*, ``PostHelper`` > **helper.blog.post**
* */helper/blog/view.py*, ``ViewHelper`` > **helper.blog.view**
* */helper/foo_bar.py*, ``FooBarHelper`` > **helper.foo_bar**


Method Invoke rules
-------------------
* */helper/foo.py*, ``def func1(self)``: **helper.foo.func1()**
* */helper/foo.py*, ``def func2(self, a)``: **helper.foo.func2(a)**
* */helper/foo.py*, ``def func3(self, a, b)``: **helper.foo.func3(a, b)**
"""


from .singleton import Singleton as dpSingleton
from .engine import Engine as dpEngine
from .loader import Loader as dpLoader


class Helper(dpEngine, dpLoader, dpSingleton):
    pass
