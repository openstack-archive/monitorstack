``memcache`` - get statistics from a memcache server
====================================================

The memcache plugin connects to a memcache server to retrieve statistics.

Usage
-----

The plugin has two optional arguments:

* ``host`` - the hostname or IP address of the memcache server
* ``port`` - the port number of the memcache server

.. code-block:: console

    Usage: monitorstack memcache [OPTIONS]

      Get memcached stats.

    Options:
      --host TEXT     memcached host to query
      --port INTEGER  memcached server port
      --help          Show this message and exit.


Example
-------

Run the plugin:

.. code-block:: console

    $ monitorstack memcache

Example output in JSON format:

.. code-block:: json

    {
      "variables": {
        "auth_cmds": 0,
        "crawler_items_checked": 0,
        "reclaimed": 0,
        "get_expired": 0,
        "curr_items": 0,
        "pid": 24627,
        "malloc_fails": 0,
        "time_in_listen_disabled_us": 0,
        "expired_unfetched": 0,
        "hash_is_expanding": false,
        "cas_hits": 0,
        "uptime": 8,
        "touch_hits": 0,
        "delete_misses": 0,
        "listen_disabled_num": 0,
        "cas_misses": 0,
        "decr_hits": 0,
        "cmd_touch": 0,
        "incr_hits": 0,
        "version": "1.4.33",
        "limit_maxbytes": 67108864,
        "total_items": 0,
        "bytes_written": 0,
        "incr_misses": 0,
        "accepting_conns": 1,
        "rusage_system": 0.014981,
        "log_watcher_sent": 0,
        "get_flushed": 0,
        "cmd_get": 0,
        "curr_connections": 4,
        "log_worker_written": 0,
        "log_watcher_skipped": 0,
        "touch_misses": 0,
        "threads": 4,
        "total_connections": 5,
        "cmd_set": 0,
        "libevent": "2.0.22-stable",
        "conn_yields": 0,
        "get_misses": 0,
        "reserved_fds": 20,
        "bytes_read": 8,
        "hash_bytes": 524288,
        "evicted_unfetched": 0,
        "cas_badval": 0,
        "cmd_flush": 0,
        "lrutail_reflocked": 0,
        "evictions": 0,
        "bytes": 0,
        "crawler_reclaimed": 0,
        "connection_structures": 5,
        "hash_power_level": 16,
        "log_worker_dropped": 0,
        "auth_errors": 0,
        "rusage_user": 0.005598,
        "time": 1493240773,
        "delete_hits": 0,
        "pointer_size": 64,
        "decr_misses": 0,
        "get_hits": 0
      },
      "message": "memcached is ok",
      "meta": {},
      "exit_code": 0,
      "measurement_name": "memcache"
    }
