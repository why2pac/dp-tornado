# -*- coding: utf-8 -*-


def run(main):
    from . import server

    server.run_server(main)
    server.wait_server()

    from . import test_controller

    test_controller.get()
    test_controller.post()
    test_controller.put()
    test_controller.delete()
    test_controller.head()

    from . import test_model_cache

    test_model_cache.sqlite_flushall_only()
    test_model_cache.sqlite_get()
    test_model_cache.sqlite_set()
    test_model_cache.sqlite_del()
    test_model_cache.sqlite_set_with_expire()
    test_model_cache.sqlite_flushdb()
    test_model_cache.sqlite_flushall()

    from . import test_m17n

    test_m17n.switch_ko()
    test_m17n.switch_en()
    test_m17n.switch_jp()

    server.stop_server()


if __name__ == '__main__':
    run(True)
