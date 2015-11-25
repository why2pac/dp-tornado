# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller as dpController


class StarterController(dpController):
    def get(self):
        params = {
            'model': self.model.calc.number.add(10, 20),
            'helper': self.helper.calc.number.div(20, 10)
        }

        self.render('index.html', params)
