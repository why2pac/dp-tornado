if (!dp) var dp = {};

dp.helper = {
    prefixize: function(path, prefix) {
        prefix = prefix || dp_prefix;

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
    req: function(o) {
        alert('not implemented yet.');
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
        }
    }
};