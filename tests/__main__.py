# -*- coding: utf-8 -*-


def run(main):
    from . import server
    from . import controller_basic

    server.run_server(main)
    server.wait_server()

    controller_basic.get()
    controller_basic.post()
    controller_basic.put()
    controller_basic.delete()
    controller_basic.head()

    server.stop_server()


if __name__ == '__main__':
    run(True)
