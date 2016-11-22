var dp = {
    init: function() {
        if (dp.ui) {
            dp.ui.init();
        }
    },
    vars: {
        prefix: undefined,
        cached: {

        }
    },
    req: function(o, oa) {
        if (!dp.helper) {
            alert('dp.helper library is required.');
            return false;
        }

        return dp.helper.req(o, oa);
    },
    alert: function(a, b, c, d, e, f, g) {
        if (!dp.ui) {
            alert('dp.helper library is required.');
            return false;
        }

        return dp.ui.util.alert(a, b, c, d, e, f, g);
    },
    noti: function(a, b, c, d) {
        if (!dp.ui) {
            alert('dp.helper library is required.');
            return false;
        }

        return dp.ui.util.noti(a, b, c, d);
    }
};

try {
    dp.vars.prefix = dp_prefix || undefined;
}
catch (e) { }
var dp_jqlib = false;
var dp_init = function(fn) {
    if (!dp_jqlib) return;
    dp_jqlib(fn);
};

try {
    // Required jQuery >= 3.0 library.
    if (jQuery && jQuery.fn.jquery && (parseFloat(jQuery.fn.jquery.split(' ')[0]) >= 3.0 || parseFloat(jQuery.fn.jquery.split(' ')[0]) <= 1.99)) {
        dp_jqlib = jQuery;
    }
} catch (e) { }

if (!dp_jqlib) {
    alert('jQuery >= 3.x library is required.');
}
else {
    dp_init(function() {
        dp.init();
    });
}

var _el = function(selector, no_cache) {
    if (!no_cache && dp.vars.cached[selector] != undefined) return dp.vars.cached[selector];

    dp.vars.cached[selector] = dp_jqlib(selector);
    return dp.vars.cached[selector];
};