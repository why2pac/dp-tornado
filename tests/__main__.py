# -*- coding: utf-8 -*-


def run(main):
    from . import server

    server.run_server(main)
    server.wait_server()

    from . import controller_basic

    controller_basic.get()
    controller_basic.post()
    controller_basic.put()
    controller_basic.delete()
    controller_basic.head()

    from . import m17n_basic

    m17n_basic.switch_ko()
    m17n_basic.switch_en()
    m17n_basic.switch_jp()

    server.stop_server()


if __name__ == '__main__':
    run(True)
