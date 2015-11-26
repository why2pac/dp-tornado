# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class CacheDecoratorController(Controller):
    def get(self, mode=None):
        if mode == 'clear':
            self.model.foo.clear()

        self.write('cache_decorator_memory : ')
        self.write(str(self.model.foo.cache_decorator_memory(10, 20, 30)))
        self.write("<br />\n")
        self.write('cache_decorator_local : ')
        self.write(str(self.model.foo.cache_decorator_local(30, 20, 10)))
