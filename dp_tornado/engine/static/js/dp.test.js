if (!dp) var dp = {};

dp.test = {
    init: function() {
        dp_assert(dp.helper.string.uniqid(), 'test-uniqid');
        dp_assert(dp.helper.string.uniqid('prefix_'), 'test-uniqid-with-prefix');
        dp_assert(dp.helper.string.uniqid('prefix_', true), 'test-uniqid-with-entropy');
        dp_assert(dp.helper.string.uniqid('prefix_', true, '-'), 'test-uniqid-with-entropy-separator');

        dp_assert(true, 'all-test-cases');
    }
};

var dp_assert = function(eq, identifier) {
    if (!eq) {
        console.log('* Assertion Failed, ' + identifier);
        dp_jqlib('body').append(dp_jqlib('<p />').addClass('assert').addClass('fail').text('* Assertion Failed, ' + identifier));

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