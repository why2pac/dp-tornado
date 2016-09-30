# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class PostController(Controller):
    def get(self):
        self.finish("""
<html>
<body>
    <form action="/post/multipart/%s/%s/article" method="post" enctype="multipart/form-data">
    <input type="file" name="file"><input type="submit">
</form>
</body>
</html>
""" % ('image', self.helper.random.uuid()))
