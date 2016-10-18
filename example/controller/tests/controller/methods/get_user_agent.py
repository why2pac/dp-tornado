# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class GetUserAgentController(Controller):
    def get(self):
        user_agents = [
            (False, 10, 7, 0, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A', '_os-mac_os_x-10.9.3 _os-mac_os_x-10 _browser-safari-7-0-3 _browser-safari-7 _device-unknown-unknown'),
            (False, 6, 6, 6, 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25', '_os-ios-6.0 _os-ios-6 _browser-safari-6-0 _browser-safari-6 _device-ipad-6.0 _device-ipad-6'),
            (False, 10, 5, 0, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2', None),

            (False, 7, 40, 0, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1', None),
            (False, 8, 36, 0, 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0', None),
            (False, 10, 33, 0, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0', None),

            (False, 7, 41, 0, 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', None),
            (False, 10, 40, 0, 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', None),
            (False, 10, 37, 0, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36', None),

            (False, 7, 11, 0, 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko', None),
            (False, 7, 10, 0, 'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0', None),
            (False, 10, 10, 0, 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)', None),
            (False, 7, 9, 0, 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)', None),
            (False, 7, 9, 0, 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)', None),
            (False, 7, 9, 0, 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)', None),
            (False, 7, 9, 0, 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)', None),
            (False, 7, 9, 0, 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0', None),
            (False, 7, 9, 0, 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)', None),
            (False, 0, 8, 0, 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; .NET CLR 2.7.58687; SLCC2; Media Center PC 5.0; Zune 3.4; Tablet PC 3.6; InfoPath.3)', None),
            (False, 2000, 7, 0, 'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0; Trident/4.0; FBSMTWB; .NET CLR 2.0.34861; .NET CLR 3.0.3746.3218; .NET CLR 3.5.33652; msn OptimizedIE8;ENUS)', None),
            (False, 7, 8, 0, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.3; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MS-RTC LM 8)', None),
            (False, 7, 8, 0, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)', None),

            (False, 4, 0, 4, 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', None),
            (False, 2, 0, 2, 'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9', None),
            (False, 2, 0, 2, 'Mozilla/5.0 (Linux; U; Android 2.3.4; fr-fr; HTC Desire Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1', None),

            (False, 0, 7, 0, 'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+', None),
            (False, 0, 7, 0, 'Mozilla/5.0 (BlackBerry; U; BlackBerry 9850; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.115 Mobile Safari/534.11+', None),

            (True, 0, 2, 0, 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', None),
            (True, 0, 2, 0, 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)', None),

            (False, 0, 0, 0, 'curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)', None),
            (False, 0, 0, 0, 'curl/7.7.x (i386--freebsd4.3) libcurl 7.7.x (SSL 0.9.6) (ipv6 enabled)', None)
        ]

        for ua in user_agents:
            pa = self.get_user_agent(user_agent=ua[4])

            assert(pa.is_bot == ua[0])
            assert(pa.os.major == ua[1])
            assert(pa.browser.major == ua[2])
            assert(pa.device.major == ua[3])

            if ua[5]:
                assert(ua[5] == pa.css)

        self.finish('done')
