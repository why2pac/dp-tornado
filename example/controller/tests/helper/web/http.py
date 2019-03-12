# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class HttpController(Controller):
    def post(self):
        print(self.get_argument('foo'))

    def get(self):
        get_url = 'https://httpbin.org/get'
        post_url = 'https://httpbin.org/post'
        patch_url = 'https://httpbin.org/patch'
        put_url = 'https://httpbin.org/put'
        delete_url = 'https://httpbin.org/delete'
        image_png_url = 'https://httpbin.org/image/png'

        # GET - TEXT

        get_code, get_res = self.helper.web.http.get.text(get_url)

        assert(get_code == 200)
        assert(get_res is not None)

        get_res = self.helper.string.serialization.deserialize(get_res, method='json')

        assert(get_res['url'] == get_url)

        # GET - JSON

        get_code, get_res = self.helper.web.http.get.json(get_url)

        assert(get_code == 200)
        assert(get_res['url'] == get_url)

        # GET - w/ Param

        get_code, get_res = self.helper.web.http.get.json(get_url, data={'foo': 'bar'})

        assert(get_code == 200)
        assert(get_res['args']['foo'] == 'bar')

        # GET - RAW (Image)

        get_code, get_res = self.helper.web.http.get.raw(image_png_url)

        assert(get_code == 200)
        assert(get_res is not None)

        from PIL import Image

        if self.helper.misc.system.py_version <= 2:
            from cStringIO import StringIO
        else:
            from io import BytesIO as StringIO

        stream = StringIO(get_res)
        img = Image.open(stream)
        img_size = img.size
        img.close()

        assert(img_size[0] > 0 and img_size[1] > 0)

        # POST - JSON

        get_code, get_res = self.helper.web.http.post.json(post_url)

        assert(get_code == 200)
        assert(get_res['url'] == post_url)

        # POST - w/ JSON

        get_code, get_res = self.helper.web.http.post.json(post_url, json={'foo': 'bar'})

        assert(get_code == 200)
        assert(get_res['json']['foo'] == 'bar')

        # POST - w/ Param (form)

        get_code, get_res = self.helper.web.http.post.json(post_url, data={'foo': 'bar'})

        assert(get_code == 200)
        assert(get_res['form']['foo'] == 'bar')

        # POST - w/ Param (form)

        get_code, get_res = self.helper.web.http.post.json(post_url, params={'foo': 'bar'})

        assert(get_code == 200)
        assert(get_res['args']['foo'] == 'bar')

        # PATCH - JSON

        get_code, get_res = self.helper.web.http.patch.json(patch_url)

        assert(get_code == 200)
        assert(get_res['url'] == patch_url)

        # PATCH - w/ Param

        get_code, get_res = self.helper.web.http.patch.json(patch_url, params={'foo': 'bar'})

        assert(get_code == 200)
        assert(get_res['args']['foo'] == 'bar')

        # PUT - JSON

        get_code, get_res = self.helper.web.http.put.json(put_url)

        assert(get_code == 200)
        assert(get_res['url'] == put_url)

        # PUT - w/ Param

        get_code, get_res = self.helper.web.http.put.json(put_url, params={'foo': 'bar'})

        assert(get_code == 200)
        assert(get_res['args']['foo'] == 'bar')

        # DELETE - JSON

        get_code, get_res = self.helper.web.http.delete.json(delete_url)

        assert(get_code == 200)
        assert(get_res['url'] == delete_url)

        # DELETE - w/ Param

        get_code, get_res = self.helper.web.http.delete.json(delete_url, params={'foo': 'bar'})

        assert(get_code == 200)
        assert(get_res['args']['foo'] == 'bar')

        self.finish('done')
