# dp-tornado

MVC Web Application Framework with Tornado, Python 2 and 3

* Python 2.7+ / 3.4+
* Linux Kernel 2.5.44+ (Epoll Required)

## Dependencies

* [tornado](http://www.tornadoweb.org) Network Library
* [SQLAlchemy](http://www.sqlalchemy.org) Model Implementation
* [hiredis](https://pypi.python.org/pypi/hiredis) Redis
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4) Screen Scrapping.
* [Croniter](https://pypi.python.org/pypi/croniter/) Croniter
* [Boto](http://docs.pythonboto.org) Boto
* [Requests](http://docs.python-requests.org) Reuqests
* [Node.js](http://www.nodejs.org) Node.JS, UglifyJS (Optional)
* [Java](http://www.java.com) Java, YUICompressor (Optional)


## Installation

### Prerequisites

	sudo yum groupinstall "Development tools"
	sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel libffi-devel
	sudo yum install python-devel
	sudo yum install postgresql-devel sqlite-devel

	mkdir /data
	mkdir /data/python

### Installing Python3.4 from Source Code

	cd /data/python

	wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
	tar -xzf Python-3.4.2.tgz Python-3.4.2-src
	cd Python-3.4.2.tgz

	./configure --prefix=/data/python/Python-3.4.2 --enable-unicode=ucs4 --with-threads
	make && make altinstall

### Installing Node.js from Binary

	cd /data/nodejs
	
	wget http://nodejs.org/dist/v0.10.33/node-v0.10.33-linux-x64.tar.gz
	tar -xzvf node-v0.10.33-linux-x64.tar.gz
	cd node-v0.10.33-linux-x64/bin
	ln -s node /usr/sbin/node

### Python Library from PIP

	pip install tornado
	pip install sqlalchemy
	pip install psycopg2
	pip install cxOracle
	pip install hiredis
	pip install beautifulsoup4
	pip install croniter
	pip install boto
	pip install requests

### Execution

**Bootstrap**

	kill -9 $(pgrep -f bootstrap.py)
	python bootstrap.py

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

**NGINX Execution**

	/etc/init.d/nginx stop
	sudo nginx
