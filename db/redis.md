### redis
- redis集群 不要在pipeline中使用mget，mset等批量处理key的操作，慎用pipeline。https://help.aliyun.com/document_detail/26356.html
  
  说明:集群实例受限的Redis命令只支持所操作key均分布在单个hash slot中的场景，没有实现多个hash slot数据的合并功能，因此需要用hash tag的方式确保要操作的key均分布在一个hash slot中。

  比如有key1，aakey，abkey3，那么我们在存储的时候需要用{key}1，aa{key}，ab{key}3的方式存储，这样调用受限命令时才能生效。具体关于hash tag的用法请参见Redis官方文档：http://redis.io/topics/cluster-spec。

  事务之前没有使用watch命令且事务中都是单key的命令场景，不再要求所有key必须在同一个slot中，使用方式和直连redis完全一致。其他场景要求事务中所有命令的所有key必须在同一个slot中。

  多key命令包括：DEL、SORT、MGET、MSET、BITOP、EXISTS、MSETNX、RENAME、 RENAMENX、BLPOP、BRPOP、RPOPLPUSH、BRPOPLPUSH、SMOVE、SUNION、SINTER、SDIFF、SUNIONSTORE、SINTERSTORE、SDIFFSTORE、ZUNIONSTORE、ZINTERSTORE、 PFMERGE、PFCOUNT。
  不允许在事务中使用的命令包括：WATCH、UNWATCH、RANDOMKEY、KEYS、SUBSCRIBE、 UNSUBSCRIBE、PSUBSCRIBE、PUNSUBSCRIBE、PUBLISH、PUBSUB、SCRIPT、EVAL、 EVALSHA、SCAN、ISCAN、DBSIZE、ADMINAUTH、AUTH、PING、ECHO、FLUSHDB、 FLUSHALL、MONITOR、IMONITOR、RIMONITOR、INFO、IINFO、RIINFO、CONFIG、 SLOWLOG、TIME、CLIENT。
