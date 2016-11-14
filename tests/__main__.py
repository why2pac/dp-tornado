# -*- coding: utf-8 -*-


def run(main):
    from . import test_cli

    test_cli.run_test()

    from . import server

    server.run_server(main)
    server.wait_server()

    from . import test_config

    test_config.config()

    from . import test_controller

    test_controller.get()
    test_controller.post()
    test_controller.put()
    test_controller.delete()
    test_controller.head()

    test_controller.methods_get_user_agent()
    test_controller.methods_get_argument()
    test_controller.methods_set_header()
    test_controller.methods_request_uri()
    test_controller.methods_redirect()
    test_controller.methods_redirect_prefix()
    test_controller.methods_finish_with_error()

    test_controller.session_sessionid()
    test_controller.session_get_and_set()

    test_controller.cookie_get_and_set()

    test_controller.prefix()

    from . import test_handler

    test_handler.exception_before()
    test_handler.exception_raise()
    test_handler.exception_after()

    from . import test_helper

    test_helper.datetime()
    test_helper.datetime_auto()
    test_helper.datetime_date()
    test_helper.datetime_time()
    test_helper.datetime_timestamp()

    test_helper.security_crypto()
    test_helper.security_crypto_encoding()
    test_helper.security_crypto_hash()
    test_helper.security_web_csrf()

    test_helper.misc_uuid()

    test_helper.numeric_random()

    test_helper.string()
    test_helper.string_cast()
    test_helper.string_check()
    test_helper.string_serialization_json()
    test_helper.string_random()

    test_helper.io_path()
    test_helper.io_file()
    test_helper.io_file_zip()

    test_helper.io_image_manipulate()

    test_helper.web_aws_s3()
    test_helper.web_aws_s3_post()
    test_helper.web_aws_dynamodb()

    test_helper.web_email()
    test_helper.web_http()
    test_helper.web_html()
    test_helper.web_url()

    test_helper.locale_korea()

    test_helper.validator_email()
    test_helper.validator_form()
    test_helper.validator_phone()
    test_helper.validator_url()

    from . import test_view_module

    test_view_module.static()
    test_view_module.pagination()
    test_view_module.pagination_prefix()

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

    from . import test_view_static

    test_view_static.js_lib_include()
    test_view_static.js_lib()
    test_view_static.js_lib_virtual()

    from . import test_scheduler

    test_scheduler.period()

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

    test_model_cache.decorator_caching()
    test_model_cache.decorator_run_alone()

    from . import test_m17n

    test_m17n.switch_ko()
    test_m17n.switch_en()
    test_m17n.switch_jp()

    server.stop_server()


if __name__ == '__main__':
    run(True)
