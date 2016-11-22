# Migration

### 0.9.3.7

* **Dynamic Cache Method Invoking**: (Breaking Change) `dsn` argument must specify when invoking a cache method. (eg. `cache.get(key, val, dsn)` must be `cache.get(key, val, dsn=dsn)`)

### 0.9.0

* **Scheduler**: (Breaking Changes) Code refactoring.
* **Helper**: (Breaking Changes) Code refactoring.
* **ui_methods**: (Breaking Changes) Code refactoring.