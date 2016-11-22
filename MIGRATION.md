# Migration


### Develop (unreleased)

* **Dynamic Cache Method Invoking**: (Breaking Change) `dsn` argument must specify when invoking a cache method. (eg. `cache.get(key, val, dsn)` must be `cache.get(key, val, dsn=dsn)`)