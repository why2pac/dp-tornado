if (!dp) var dp = {};

dp.ui = {
    _initiated: false,
    init: function(obj) {
        if (!obj && dp.ui._initiated) return;
        dp.ui._initiated = true;
        dp.ui.element.init(obj);
    },
    util: {
        alert: function(a, b, c, d, e, f, g) {
            alert('not implemented yet.');
        },
        noti: function(a, b, c, d) {
            alert('not implemented yet.');
        }
    },
    element: {
        init: function(obj) {
            dp.ui.element.input.delegate.on_return(obj);
            dp.ui.element.input.delegate.on_focus(obj);
        },
        input: {
            delegate: {
                on_return: function(obj) {
                    if (!obj) obj = dp_jqlib('body');
                    obj.find('input[dp-on-return][dp-on-return-installed!=yes]').each(function() {
                        var _id = dp_jqlib(this).attr('id') || 'uniqid-' + dp.helper.string.uniqid();

                        dp_jqlib(this).attr('id', _id);
                        dp_jqlib(this).attr('dp-on-return-installed', 'yes');

                        dp_jqlib(this).keypress(function(e) {
                            if (dp_jqlib(this).attr('dp-on-return-busy') == 'yes') {
                                return;
                            }

                            if (e.keyCode == 13) {
                                dp_jqlib(this).attr('dp-on-return-busy', 'yes');
                                setTimeout(dp_jqlib(this).attr('dp-on-return'), 0);
                                setTimeout("dp_jqlib('#" + _id + "').attr('dp-on-return-busy', 'no');", 150);

                                e.preventDefault();
                            }
                        });
                    });
                },
                on_focus: function(obj) {
                    if (!obj) obj = dp_jqlib('body');
                    obj.find('input[dp-on-focus][dp-on-focus-installed!=yes]').each(function() {
                        var _id = dp_jqlib(this).attr('id') || 'uniqid-' + dp.helper.string.uniqid();

                        dp_jqlib(this).attr('id', _id);
                        dp_jqlib(this).attr('dp-on-focus-installed', 'yes');

                        dp_jqlib(this).focus(function(e) {
                            setTimeout(dp_jqlib(this).attr('dp-on-focus'), 0);
                        });
                    });
                }
            }
        }
    }
};

dp_init(function() {
    dp.init();
});