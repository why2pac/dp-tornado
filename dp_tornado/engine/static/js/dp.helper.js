if (!dp) var dp = {};

dp.helper = {
    prefixize: function(path, prefix) {
        prefix = prefix || dp.vars.prefix;

        if (prefix) {
            if (dp.helper.string.endsWith(prefix, '/')) {
                prefix = prefix.substr(0, prefix.length -1);
            }
        }
        else {
            prefix = '';
        }

        if (dp.helper.string.startsWith(path, prefix)) {
            path = path.substr(prefix.length) || '/';
        }

        return path;
    },
    req_busy: {},
    req: function(obj, obj_add) {
        if (obj instanceof dp_jqlib) {
            var _obj = obj;
            obj = {
                'url': _obj.attr('action'),
                'type': _obj.attr('method'),
                'dataType': obj.attr('dp-req-res-type') || 'json',
                'prefixize': obj.attr('dp-req-prefixize') != 'no' && obj.attr('dp-req-prefixize') != 'false',
                'fields': []
            };

            if (_obj.find('*[dp-req-type="button"]').length > 0) {
                var _btn = dp_jqlib(_obj.find('*[dp-req-type="button"]').get(0));

                obj.button = _btn;
                obj.fade = _btn.attr('dp-req-fade') != 'no' && _btn.attr('dp-req-fade') != 'false';
                obj.multiple = _btn.attr('dp-req-multiple') != 'no' && _btn.attr('dp-req-multiple') != 'false';

                if (!_btn.attr('dp-req-identifier')) {
                    _btn.attr('dp-req-identifier', 'req-' + dp.helper.string.uniqid());
                }

                if (_btn.attr('dp-req-identifier')) {
                    obj.identifier = _btn.attr('dp-req-identifier');
                }
            }

            _obj.find('*[dp-req-type]').each(function(i, e) {
                var _this = dp_jqlib(this);
                obj.fields.push({
                    'name': _this.attr('name') || _this.attr('id'),
                    'obj': _this,
                    'required': _this.attr('dp-req-required') == 'yes' || _this.attr('dp-req-required') == 'true',
                    'focus': _this.attr('dp-req-required') == 'yes' || _this.attr('dp-req-required') == 'true',
                    'validate': _this.attr('dp-req-type'),
                    'length': _this.attr('dp-req-length') ? dp_jqlib.map(_this.attr('dp-req-length').split(','), function(v, i) { return parseInt(v, 10); }) : undefined,
                    'message': {
                        'missing': _this.attr('dp-req-missing'),
                        'invalid': _this.attr('dp-req-invalid'),
                        'confirm': _this.attr('dp-req-confirm')
                    }
                });
            });
        }

        if (obj_add) {
            dp_jqlib.extend(obj, obj_add);
        }

        var btn = obj.button || undefined;
        var multiple = obj.multiple || false;
        var fields = obj.fields || [];
        var url = obj.url || undefined;
        var type = obj.type || 'POST';
        var data = obj.data || {};
        var dataType = obj.dataType || 'json';
        var fade = obj.fade != undefined ? obj.fade : true;
        var prefixize = obj.prefixize != undefined ? obj.prefixize : true;
        var prefix = obj.prefix != undefined ? obj.prefix : dp.vars.prefix;
        var identifier = obj.identifier || undefined;
        var opacity_origin = btn ? btn.css('opacity') : 1.0;

        if (btn && !btn.attr('id')) {
            btn.attr('id', 'temp-' + dp.helper.string.uniqid());
        }

        if (!identifier) {
            identifier = btn ? btn.attr('id') : dp.helper.string.uniqid();
        }

        if (!multiple && dp.helper.req_busy[identifier]) return false;
        dp.helper.req_busy[identifier] = true;

        var no_finalize = false;
        var fn_finalize = function() {
            if (no_finalize) {
                no_finalize = false;
                return;
            }

            dp.helper.req_busy[identifier] = false;
            if (btn) {
                btn.fadeTo(100, opacity_origin);
            }
        };

        if (obj.before) {
            if (obj.before() == false) {
                fn_finalize();
                return false;
            }
        }

        var fields_checked = true;
        var output = false;

        dp_jqlib(fields).each(function(i, e) {
            var val = e.obj.val();
            var skip = false;

            // Required
            if (fields_checked && e.required && !val) {
                if (e.message && e.message.missing) {
                    output = dp.alert(e.message.missing);
                }

                fields_checked = false;
            }

            // Button - SKIP
            if (fields_checked && e.validate == 'button') {
                skip = true;
            }
            // E-Mail validation
            else if (fields_checked && e.validate == 'email' && !dp.helper.validator.email(val)) {
                if (e.message && e.message.invalid) {
                    output = dp.alert(e.message.invalid);
                }

                fields_checked = false;
            }
            // URL validation
            else if (fields_checked && e.validate == 'url' && !dp.helper.validator.url(val)) {
                if (e.message && e.message.invalid) {
                    output = dp.alert(e.message.invalid);
                }

                fields_checked = false;
            }

            if (fields_checked && e.length) {
                if ((e.length.length >= 1 && val.length < e.length[0]) || (e.length.length >= 2 && val.length > e.length[1])) {
                    if (e.message && e.message.invalid) {
                        output = dp.alert(e.message.invalid);
                    }

                    fields_checked = false;
                }
            }

            // Confirm (alert)
            if (fields_checked && e.message && e.message.confirm && !e.message.confirming) {
                e.message.confirming = true;
                output = dp.alert(
                    e.message.confirm,
                    function() {
                        fn_finalize();
                        dp.req(obj);
                    },
                    function() {
                        fn_finalize();
                    }
                );

                no_finalize = true;
                fields_checked = false;
            }

            if (!fields_checked) {
                dp.ui.util.alert_focus = e.obj;
                return false;
            }

            if (!skip && e.name) {
                data[e.name] = val;
            }
        });

        if (!fields_checked) {
            fn_finalize();
            return output;
        }

        var finalize = function(data) {
            if (data && typeof(data) == 'object') {
                if (data.message) {
                    dp.alert(data.message, function() {
                        if (data.redirect) {
                            document.location.href = data.redirect;
                        }
                    });
                }
            }
        };

        var success = function(res) {
            if (dataType && dataType.toLowerCase() == 'json') {
                if (res.result != undefined && !res.result) {
                    error(undefined, undefined, undefined, res);
                    return;
                }
            }

            fn_finalize();

            if (obj.success) {
                obj.success(res, data);
            }

            finalize(res);
        };

        var error = function(a, b, c, res) {
            fn_finalize();

            if (obj.error) {
                obj.error(res, a, b, c);
            }

            finalize(res);
        };

        var ajax_req = function() {
            var payload = {
                url: prefixize ? dp.helper.prefixize(url, prefix) : url,
                type: type,
                data: data,
                dataType: dataType,
                success: success,
                error: error
            };

            dp_jqlib.ajax(payload);
        };

        if (btn && fade) {
            btn.stop().clearQueue().fadeTo(100, 0.3, function() {
                ajax_req();
            });
        }
        else {
            ajax_req();
        }

        return true;
    },
    validator: {
        email: function(e) {
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(e);
        },
        url: function(e, i) {
            if (!i && e.indexOf('http')) {
                return false;
            }

            var re = new RegExp('^(?:(?:https?|ftp)://)(?:\\S+(?::\\S*)?@)?(?:(?!(?:10|127)(?:\\.\\d{1,3}){3})(?!(?:169\\.254|192\\.168)(?:\\.\\d{1,3}){2})(?!172\\.(?:1[6-9]|2\\d|3[0-1])(?:\\.\\d{1,3}){2})(?:22[0-3]|2[01]\\d|[1-9]\\d?|1\\d\\d)(?:\\.(?:25[0-5]|2[0-4]\\d|1?\\d{1,2})){2}(?:\\.(?:25[0-4]|2[0-4]\\d|1\\d\\d|[1-9]\\d?))|(?:(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-z\\u00a1-\\uffff]{2,})))(?::\\d{2,5})?(?:/\\S*)?$', 'i');
			return re.test(e);
        }
    },
    string: {
        _uniqid_seed: 0,
        uniqid: function(prefix, more_entropy, more_entropy_separator) {
            /* This code has extracted from php.js */

            if (!prefix) {
                prefix = "";
            }

            if (!more_entropy_separator) {
                more_entropy_separator = '';
            }

            var retId;
            var formatSeed = (function(seed, reqWidth){
                seed = parseInt(seed, 10).toString(16);

                if (reqWidth < seed.length)
                {
                    return seed.slice(seed.length - reqWidth);
                }

                if (reqWidth > seed.length)
                {
                    var arr = new Array(1 + (reqWidth - seed.length));
                    return arr.join('0') + seed;
                }

                return seed;
            });

            if (!dp.helper.string._uniqid_seed)
            {
                dp.helper.string._uniqid_seed = Math.floor(Math.random() * 0x75bcd15);
            }

            dp.helper.string._uniqid_seed++;

            retId = prefix; // start with prefix, add current milliseconds hex string
            retId += formatSeed(parseInt(new Date().getTime() / 1000, 10), 8);
            retId += formatSeed(dp.helper.string._uniqid_seed, 5); // add seed hex string

            // for more entropy we add a float lower to 10
            if (more_entropy)
            {
                retId += (Math.random() * 10).toFixed(8).toString();
            }

            return dp.helper.string.replaceAll(retId, '.', more_entropy_separator);
        },
        replaceAll: function(text, find, replace) {
            return text.split(find).join(replace);
        },
        startsWith: function(str, prefix) {
            return str ? str.indexOf(prefix, 0) !== -1 : false;
        },
        endsWith: function(str, suffix) {
            return str ? str.indexOf(suffix, str.length - suffix.length) !== -1 : false;
        },
        extract_numbers: function(val) {
            var replace = /[^0-9]/gi;
            return (val.substring(0, 1) == '-' ? '-' : '') + val.replace(replace, '');
        },
        number_format: function(val) {
            return val.toFixed(0).replace(/(\d)(?=(\d{3})+$)/g, "$1,");
        }
    }
};