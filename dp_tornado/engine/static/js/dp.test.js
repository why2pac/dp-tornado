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
        }, wait * 2);
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