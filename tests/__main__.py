# -*- coding: utf-8 -*-


def run(main):
    from . import server

    server.run_server(main)
    server.wait_server()

    server.stop_server()


if __name__ == '__main__':
    run(True)
