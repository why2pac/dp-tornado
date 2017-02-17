# Migration

### 0.9.4.8

* **cli > `ini`**: Argument added. You can the specify config.ini file name as a cli argument.
* **cli > `mode`**: Argument removed. Use config.ini instead of `mode` cli argument. 

### 0.9.4.1

* **Docker**: Support docker images. Find out more information about dp4p docker, [Here, http://hub.docker.com/r/why2pac/dp4p](http://hub.docker.com/r/why2pac/dp4p).
* **config.ini > app.mode**: Identify app mode from your code. (eg. `debug = True if ini.app.mode == 'test' else False`, default value is `'NOT SET'`)
* **config.ini > logging.dp**: `logging.debug`, `logging.info`, `logging.warning`, `logging.error`, from this version, has a separate logger name. (`logging.dp` value is used logging level value.) 

### 0.9.3.7

* **Dynamic Cache Method Invoking**: (Breaking Change) `dsn` argument must specify when invoking a cache method. (eg. `cache.get(key, val, dsn)` must be `cache.get(key, val, dsn=dsn)`)

### 0.9.0

* **Scheduler**: (Breaking Changes) Code refactoring.
* **Helper**: (Breaking Changes) Code refactoring.
* **ui_methods**: (Breaking Changes) Code refactoring.
