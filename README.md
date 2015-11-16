# dp-tornado

MVC Web Application Framework with Tornado, Python 2 and 3

* Python 2.7+ / 3.4+
* Linux Kernel 2.5.44+, If epoll enabled

## Dependencies

* [tornado](http://www.tornadoweb.org) Network Library
* [SQLAlchemy](http://www.sqlalchemy.org) Model Implementation
* [redis](https://github.com/andymccurdy/redis-py) Redis
* [Croniter](https://pypi.python.org/pypi/croniter/) Scheduler
* [Boto](http://docs.pythonboto.org) AWS Helper
* [Requests](http://docs.python-requests.org) HTTP Reuqest
* [Node.js](http://www.nodejs.org) Node.JS, UglifyJS (Optional)
* [Java](http://www.java.com) Java, YUICompressor (Optional)


### Deployment

**NGINX Configuration**

	upstream dp_proxy {
		server 127.0.0.1:22001;
	}
	
	server {
		listen                  80;
		server_name             dp_for_tornado;
		
		client_max_body_size    50M;
		
		rewrite ^/s/(.*)$ /static/$1 last;
		
		location ~ /\. { deny  all; }
		
		location ~ /pp_(?:40[345]|5xx)[.]html$ {
			root    /data/dist/prepared-pages/;
		}
		
		location ^~ /static/ {
			access_log          off;
			log_not_found       off;
			expires             max;
			
			add_header Pragma public;
			add_header Cache-Control "public, must-revalidate, proxy-revalidate";
			
			root    /data/dist/dp-tornado/;
		}
		
		location / {
			proxy_pass_header       Server;
			proxy_set_header        Host $http_host;
			proxy_redirect          off;
			proxy_set_header        X-Real-IP $remote_addr;
			proxy_set_header        X-Scheme $scheme;
			proxy_set_header        X-Proxy-Prefix '/foo/';
			proxy_pass              http://dp_proxy/foo/;
		}
		
		error_page 403 /pp_403.html;
		error_page 404 /pp_404.html;
		error_page 405 /pp_405.html;
		error_page 500 501 502 503 504 /pp_5xx.html;
	}
