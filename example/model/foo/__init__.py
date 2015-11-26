# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class FooModel(dpModel):
    @dpModel.cache(10)
    def cache_decorator_memory(self, a, b, c):
        return a+b+c+self.helper.random.randint(0, 10**7)

    @dpModel.cache('foo.bar/memory', 10)
    def cache_decorator_local(self, a, b, c):
        return a+b+c+self.helper.random.randint(0, 10**7)
