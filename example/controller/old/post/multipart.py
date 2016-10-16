# -*- coding: utf-8 -*-


import os
import tempfile

import tornado.web
import tornado.gen
import tornado.concurrent
import tornado.options
import functools

from dp_tornado.engine.handler import Handler as dpHandler

executor = tornado.concurrent.futures.ThreadPoolExecutor(50)


def run_on_executor(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        callback = kwargs.pop("callback", None)
        future = executor.submit(fn, self, *args, **kwargs)
        if callback:
            self.io_loop.add_future(future, lambda future: callback(future.result()))
        return future
    return wrapper


@tornado.web.stream_request_body
class MultipartHandler(dpHandler):
    def get(self, *args, **kwargs):
        self.finish('xxx')

    @tornado.concurrent.run_on_executor
    def post(self, *args, **kwargs):
        pass

    @tornado.concurrent.run_on_executor
    def process(self):
        # 임시파일을 생성하지 못했을 경우 종료
        if not self.tempfile:
            return

        deferred = {
            'files': []
        }

        try:
            if self.type == 'image':
                self.process_image(deferred)
        except Exception as e:
            self.model.post.status.set(self.action_identifier, 'error', 'process', 'exception')

            import traceback
            traceback.print_exc()

            self.logging.warning(e)

        # Temporary 파일 제거 (업로드)
        try:
            self.tempfile.close()
        except:
            pass

        # Temporary 파일 제거 (임의 생성)
        for file in deferred['files']:
            try:
                os.remove(file)
            except:
                pass

    def process_image(self, deferred):
        # 전처리 (업로드 Type에 따른 올바른 형식인지 확인)
        self.model.post.status.set(self.action_identifier, 'uploading', 'check')

        if os.path.getsize(self.tempfile.name) <= 0:
            self.model.post.status.set(self.action_identifier, 'error', 'empty')
            return

        try:
            from PIL import Image
            uploaded_img = Image.open(self.tempfile.name)
        except IOError:
            self.model.post.status.set(self.action_identifier, 'error', 'image', 'invalid')
            return

        width, height = uploaded_img.size
        ext = str(uploaded_img.format).lower()

        if ext not in ('jpeg', 'jpg', 'gif', 'png'):
            self.model.post.status.set(self.action_identifier, 'error', 'ext', 'invalid')
            return

        if ext == 'jpeg':
            ext = 'jpg'

        thumb = None
        large = None

        filename = '%s-%s-%s-%s_%s' % (
            self.helper.datetime.date.year(),
            self.helper.datetime.date.month(),
            self.helper.datetime.date.day(),
            self.helper.datetime.time.hhiiss(),
            self.helper.security.crypto.hash.sha224('%sx%s' % (width, height)))

        filename_thumb = '%s_thumb.%s' % (filename, ext)
        filename_large = '%s_large.%s' % (filename, ext)
        filename = '%s.%s' % (filename, ext)

        print(self.tempfile)
        print(self.tempfile.name)

        """
        s3bridge = self.helper.aws.s3.connect(self.config.aws.access_key.id, self.config.aws.access_key.secret)
        s3bridge.set_contents_from_file(self.config.aws.bucket.temporary.key, filename, self.tempfile)

        if thumb:
            s3bridge.set_contents_from_file(self.config.aws.bucket.temporary.key, filename_thumb, thumb)

        if large:
            s3bridge.set_contents_from_file(self.config.aws.bucket.temporary.key, filename_large, large)

        self.model.post.status.set(
            self.action_identifier, 'uploaded', self.config.aws.bucket.temporary.endpoint, filename, width, height)
        """

    def prepare(self):
        request_uri = self.request.uri.split('/post/multipart/')[1].split('/')

        self.type = request_uri[0] if len(request_uri) > 0 else None
        self.action_identifier = request_uri[1] if len(request_uri) > 1 else None
        self.options = request_uri[2] if len(request_uri) > 2 else None
        self.content_length = self.request.headers['Content-Length'] if 'Content-Length' in self.request.headers else 0
        self.content_length = self.helper.numeric.cast.long(self.content_length)
        self.received_length = 0
        self.stx = None
        self.btx = None
        self.etx = None

        import toro
        import threading

        print('>', request_uri)
        print('>', self.type)
        print('>', self.action_identifier)
        print('>', self.options)

        self.buffer = toro.Queue()
        self.lval = False
        self.lock = threading.Lock()

        try:
            self.tempfile = tempfile.NamedTemporaryFile(mode='w+b', delete=False)

        except:
            self.tempfile = None

        if self.tempfile:
            self.model.post.status.set(self.action_identifier, 'uploading', 'prepared')

        else:
            self.model.post.status.set(self.action_identifier, 'error', 'tempfile', 'create')

    @tornado.gen.coroutine
    def data_received(self, chunk):
        yield self.buffer.put(chunk)
        self.producer()

    @run_on_executor
    def producer(self):
        if not self.tempfile:
            return

        if self.lval:
            return

        self.lval = True

        if self.lock.locked():
            return

        self.lock.acquire()

        try:
            chunk = self.buffer.get_nowait()
        except Exception as e:
            print(e)
            return

        self.received_length += len(chunk)

        if not self.stx or not self.etx:
            chunks = chunk.splitlines()
            stx = chunks[0]
            etx = stx + '--'

            self.stx = stx
            self.etx = etx
            self.btx = chunk.find(stx)

            f = False
            x = None
            for c in chunks:
                if f == True:
                    x = c
                    break

                if c == '':
                    f = True

            self.btx = chunk.find(x)

        stx = self.stx
        etx = self.etx

        stx = True if chunk.find(stx) == 0 else False
        etx = True if chunk.find(etx) != -1 else False

        if stx and not etx:
            chunk = chunk[self.btx:]

        elif not stx and etx:
            chunk = chunk[0:chunk.find(self.etx)]

            if chunk.endswith('\r\n'):
                chunk = chunk[:-2]
            elif chunk.endswith('\n'):
                chunk = chunk[:-1]
            elif chunk.endswith('\r'):
                chunk = chunk[:-1]

        elif not stx and not etx:
            pass

        elif stx and etx:
            chunk = chunk[self.btx:chunk.find(self.etx)]

            if chunk.endswith('\r\n'):
                chunk = chunk[:-2]
            elif chunk.endswith('\n'):
                chunk = chunk[:-1]
            elif chunk.endswith('\r'):
                chunk = chunk[:-1]

        self.tempfile.write(chunk)

        self.model.post.status.set(
            self.action_identifier, 'uploading', 'streaming', self.received_length, self.content_length)

        if self.received_length == self.content_length:
            self.tempfile.flush()
            self.process()

        self.lock.release()
        self.lval = False

        if self.buffer.qsize() > 0:
            self.producer()
