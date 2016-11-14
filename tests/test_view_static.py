# -*- coding: utf-8 -*-


try:
    from . import utils
except (ValueError, SystemError):
    import utils

try:
    from . import consts
except (ValueError, SystemError):
    import consts


def js_lib_include():
    utils.expecting_text('get', '/view/static/js_lib/include', None, 200)


def js_lib():
    utils.expecting_text('get', '/view/static/js_lib', None, 200)


def js_lib_virtual():
    from selenium import webdriver

    driver = webdriver.PhantomJS()
    driver.get('%s/view/static/js_lib' % consts.dp_testing_path)

    assert len(driver.find_elements_by_tag_name('html')) == 1

    import time
    time.sleep(5)

    h3 = driver.find_element_by_tag_name('h3')

    time.sleep(2)

    assert h3.text == 'succeed'
