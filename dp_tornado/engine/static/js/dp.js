var dp = {
    init: function() {
    }
};

var dp_jqlib = false;
var dp_init = function(fn) {
    if (!dp_jqlib) return;
    dp_jqlib(fn);
};

try {
    // Required jQuery >= 3.0 library.
    if (jQuery && jQuery.fn.jquery && parseFloat(jQuery.fn.jquery.split(' ')[0]) >= 3.0) {
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