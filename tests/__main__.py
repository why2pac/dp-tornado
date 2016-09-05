# -*- coding: utf-8 -*-


def run():
    from . import server

    server.run_server()
    server.wait_server()

    server.stop_server()


run()
