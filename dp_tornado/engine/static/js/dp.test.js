if (!dp) var dp = {};

dp.test = {
    failed: false,
    init: function() {
        var wait = 10;

        dp_assert(function() {
            return _el('#input-test').length;
        }, 'test-el');

        dp_assert(dp.helper.string.uniqid(), 'test-uniqid');
        dp_assert(dp.helper.string.uniqid('prefix_'), 'test-uniqid-with-prefix');
        dp_assert(dp.helper.string.uniqid('prefix_', true), 'test-uniqid-with-entropy');
        dp_assert(dp.helper.string.uniqid('prefix_', true, '-'), 'test-uniqid-with-entropy-separator');

        dp_prefix = '/front';

        dp_assert(dp.helper.prefixize('/front') === '/', 'helper-prefixize-global-prefix');
        dp_assert(dp.helper.prefixize('/front/') === '/', 'helper-prefixize-global-prefix');
        dp_assert(dp.helper.prefixize('/front/foo/bar') === '/foo/bar', 'helper-prefixize-global-prefix');

        dp_prefix = undefined;

        dp_assert(dp.helper.prefixize('/front/foo/bar') === '/front/foo/bar', 'helper-prefixize-no-prefix');
        dp_assert(dp.helper.prefixize('/front/foo/bar', '/front') === '/foo/bar', 'helper-prefixize-with-prefix');
        dp_assert(dp.helper.prefixize('/front/foo/bar', '/front/') === '/foo/bar', 'helper-prefixize-with-prefix-slash');
        dp_assert(dp.helper.prefixize('/front', '/front') === '/', 'helper-prefixize-with-prefix');
        dp_assert(dp.helper.prefixize('/front', '/front/') === '/', 'helper-prefixize-with-prefix-slash');

        dp_assert(dp.helper.validator.email('email@valid.com'), 'helper-validator-email');
        dp_assert(dp.helper.validator.email('email@.invalid.com') == false, 'helper-validator-email');

        dp_assert(dp.helper.validator.url('http://www.google.com'), 'helper-validator-url');
        dp_assert(dp.helper.validator.url('http://www.google'), 'helper-validator-url');
        dp_assert(dp.helper.validator.url('http://123.123.123.123'), 'helper-validator-url');
        dp_assert(dp.helper.validator.url('http://123.123.123.256') == false, 'helper-validator-url');
        dp_assert(dp.helper.validator.url('https://www.google.') == false, 'helper-validator-url');

        dp_assert(dp.helper.string.replaceAll('abcd', 'a', '-') === '-bcd', 'helper-string-replaceAll');

        var a_wait = wait * 60;
        var a_done = 550;

        setTimeout(function() {
            var a1 = dp.alert('text message', 'Okay');

            setTimeout(function () {
                dp_assert(a1.length > 0, 'helper-alert-msg-confirm');
                dp_jqlib(a1.find('button').get(0)).trigger('click');
            }, a_done);
        }, 10);

        setTimeout(function() {
            var a2_done = false;
            var a2 = dp.alert('text message\nwith confirm delegate', function() { a2_done = true; });

            setTimeout(function() {
                dp_jqlib(a2.find('button').get(0)).trigger('click');
                dp_assert(a2_done, 'helper-alert-msg-cf-delegate');
            }, a_done);
        }, a_wait);

        setTimeout(function() {
            var a3_done = false;
            var a3 = dp.alert('text message with\nconfirm and dismiss delegate', function() { a3_done = false; }, function() { a3_done = true; });

            setTimeout(function() {
                dp_jqlib(a3.find('button').get(1)).trigger('click');
                dp_assert(a3_done, 'helper-alert-msg-cf-delegate-ds-delegate');
            }, a_done);
        }, a_wait * 2);

        setTimeout(function() {
            var a4_done = false;
            var a4 = dp.alert('text message with\nconfirm text and delegate,\ndismiss delegate', function() { a4_done = true; }, 'Okay', function() { a4_done = false; });

            setTimeout(function() {
                a4.find('button').each(function(i, e) {
                    if (dp_jqlib(e).text() == 'Okay') {
                        dp_jqlib(e).trigger('click');
                        return false;
                    }
                });
                dp_assert(a4_done, 'helper-alert-msg-cf-text-delegate-ds-delegate');
            }, a_done);
        }, a_wait * 3);

        setTimeout(function() {
            var a5_done = false;
            var a5 = dp.alert('text message with\nconfirm text and delegate,\ndismiss text and delegate', function() { a5_done = false; }, 'Okay', function() { a5_done = true; }, 'Dismiss');

            setTimeout(function() {
                a5.find('button').each(function(i, e) {
                    if (dp_jqlib(e).text() == 'Dismiss') {
                        dp_jqlib(e).trigger('click');
                        return false;
                    }
                });
                dp_assert(a5_done, 'helper-alert-msg-cf-text-delegate-ds-text-delegate');
            }, a_done);
        }, a_wait * 4);

        setTimeout(function() {
            var a6_done = false;
            var a6 = dp.alert({
                'message': 'html message <b>this is bold</b>',
                'html': true,
                'buttons': [
                    ['button 1', function() {
                        a6_done = false;
                    }],
                    ['button 2', function() {
                        a6_done = true;
                    }],
                    ['button 3', function() {
                        a6_done = false;
                    }]
                ]
            });

            setTimeout(function() {
                a6.find('button').each(function(i, e) {
                    if (dp_jqlib(e).text() == 'button 2') {
                        dp_jqlib(e).trigger('click');
                        return false;
                    }
                });
                dp_assert(a6_done, 'helper-alert-custom');
            }, a_done);
        }, a_wait * 5);

        dp_assert(
            function() {
                return dp.test.ui.element.input.delegate.on_focus_called;
            },
            'test-ui-element-input-delegate-on-focus',
            function() {
                _el('#input-test').focus();
            },
            wait
        );

        dp_assert(
            function() {
                return dp.test.ui.element.input.delegate.on_return_called;
            },
            'test-ui-element-input-delegate-on-return',
            function() {
                var e = dp_jqlib.Event('keypress');
                e.keyCode = 13;

                _el('#input-test').trigger(e);
            },
            wait
        );

        setTimeout(function() {
            dp_assert(!dp.test.failed, 'all-test-cases');
        }, wait * 500);
    },
    ui: {
        element: {
            input: {
                delegate: {
                    on_return_called: false,
                    on_return: function() {
                        dp.test.ui.element.input.delegate.on_return_called = true;
                        console.log('* dp.test.ui.element.input.delegate.on_return called.');
                    },
                    on_focus_called: false,
                    on_focus: function() {
                        dp.test.ui.element.input.delegate.on_focus_called = true;
                        console.log('* dp.test.ui.element.input.delegate.on_focus called.');
                    }
                }
            }
        }
    }
};

var dp_assert = function(eq, identifier, before, delay) {
    if (before) {
        before();
    }

    if (delay) {
        setTimeout(function() {
            dp_assert(eq, identifier);
        }, delay);
        return;
    }

    if (typeof eq == 'function') {
        eq = eq();
    }

    if (!eq) {
        if (dp.test.failed) return;

        console.log('* Assertion Failed, ' + identifier);
        dp_jqlib('body').append(dp_jqlib('<p />').addClass('assert').addClass('fail').text('* Assertion Failed, ' + identifier));
        dp.test.failed = true;

        throw new Error('* Assertion Failed, ' + identifier);
    }
    else {
        console.log('* Assertion Succeed, ' + identifier);
        dp_jqlib('body').append(dp_jqlib('<p />').addClass('assert').addClass('succ').text('* Assertion Succeed, ' + identifier));
    }
};

dp_init(function() {
    dp.test.init();
});