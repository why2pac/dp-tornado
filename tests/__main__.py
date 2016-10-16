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

    from . import test_helper

    test_helper.datetime()
    test_helper.datetime_date()
    test_helper.datetime_time()
    test_helper.datetime_timestamp()

    test_helper.security_crypto()
    test_helper.security_crypto_encoding()
    test_helper.security_crypto_hash()

    test_helper.string_serialization_json()

    test_helper.locale_korea()

    from . import test_view_ui_methods

    test_view_ui_methods.engine()
    test_view_ui_methods.yyyymmdd()
    test_view_ui_methods.mmdd()
    test_view_ui_methods.hhiiss()
    test_view_ui_methods.hhii()
    test_view_ui_methods.weekday()
    test_view_ui_methods.get()
    test_view_ui_methods.get_with_param()
    test_view_ui_methods.nl2br()
    test_view_ui_methods.number_format()
    test_view_ui_methods.request_uri()
    test_view_ui_methods.trim()
    test_view_ui_methods.truncate()

    from . import test_schema

    test_schema.migrate()

    from . import test_model_db

    test_model_db.mysql()

    from . import test_model_cache

    test_model_cache.sqlite_flushall_only()
    test_model_cache.sqlite_get()
    test_model_cache.sqlite_set()
    test_model_cache.sqlite_del()
    test_model_cache.sqlite_set_with_expire()
    test_model_cache.sqlite_flushdb()
    test_model_cache.sqlite_flushall()

    test_model_cache.redis_flushall_only()
    test_model_cache.redis_get()
    test_model_cache.redis_set()
    test_model_cache.redis_del()
    test_model_cache.redis_set_with_expire()
    test_model_cache.redis_flushdb()
    test_model_cache.redis_flushall()

    from . import test_m17n

    test_m17n.switch_ko()
    test_m17n.switch_en()
    test_m17n.switch_jp()

    server.stop_server()


if __name__ == '__main__':
    run(True)
