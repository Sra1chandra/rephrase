## Caching

The cache uses Redis. In most cases it cuts latency by up to 60%. Users do not get stale data.

A write invalidates the cache. If you use the bulk import endpoint (`POST /v2/import`), you may need to call `cache.flush()` after it. Bulk writes are not tracked by the invalidation hooks.

The default TTL is 300 seconds. Override it with the `CACHE_TTL` environment variable.
