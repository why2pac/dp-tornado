# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class DownloadController(Controller):
    def get(self):
        try:
            from urllib.request import urlopen
        except ImportError:
            from urllib import urlopen

        for i in range(3):
            url = 'https://github.com/uglide/RedisDesktopManager/releases/download/0.8.2/redis-desktop-manager-0.8.2-2549.dmg'
            downloaded = urlopen(url)

            print(downloaded)

        self.finish('done')
