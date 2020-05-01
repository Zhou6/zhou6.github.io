redis业务处理是单线程，多个客户端连接通过epoll（一个线程循环epoll_wait）方式接收请求
可以开启多个redis实例，根据key的不同分配到不同的实例，相当于压力拆分

多个连接之间的请求不能保证顺序，所以可能造成本来先处理的请求变到了后面去处理，为了解决这个问题，可以加锁，但是不好用，
另一个方法就是对应的key匹配只有一个服务能够处理这个key的操作，

### 安装redis
1. wget http://download.redis.io/releases/redis-5.0.8.tar.gz
2. 解压并进入文件夹，tar -xf 打开readme，里面有安装教程
3. vi makefile， 看内容
4. cd src => makefile
5. 编译安装
    make
    make PREFIX=~/tools/redis5 install
6. 配置环境变量   
    https://www.jianshu.com/p/7e30b7b7ee48 
    vim ~/.bashrc
        export REDIS_HOME=~/tools/redis5
        export PATH=$PATH:$REDIS_HOME/bin
    source ~/.bashrc
7. 启动服务
    cd utils => bash install_server.sh
    配置文件：/etc/redis/6379.conf
    日志：/var/log/redis_6379.log
    数据目录（持久化）：/var/lib/redis/6379
    Port           : 6379
```
Config file    : /etc/redis/6379.conf
Log file       : /var/log/redis_6379.log
Data dir       : /var/lib/redis/6379
Executable     : /Users/zhou6/tools/redis5/bin/redis-server
Cli Executable : /Users/zhou6/tools/redis5/bin/redis-cli
```


### redis集群、双副本、代理模式：
- 集群：每个节点的key都是不同的，最上面有个负载分配的东西，导致可能是用hash来计算每个key去往哪个节点，相当于分片，提高吞吐量。集群不好的一点就是部分命令无法使用，尤其是批量处理的命令（mset。。），因为多个key可能处在不同的节点，https://help.aliyun.com/document_detail/145968.html?spm=a2c4e.11153940.0.0.61a6794emr1lIx
- 副本：就是每个节点里有两个库，数据是完全一致的，容灾，防止某一台机器挂掉
- 代理模式：支持通过一个统一的连接地址（域名）访问Redis集群，客户端的请求通过代理服务器转发到各数据分片，代理服务器、数据分片和配置服务器均不提供单独的连接地址，降低了应用开发难度和代码复杂度。
- 直连模式：因所有请求都要通过代理服务器转发，代理模式在降低业务开发难度的同时也会小幅度影响Redis服务的响应速度。如果业务对响应速度的要求非常高，您可以使用直连模式，绕过代理服务器直接连接后端数据分片，从而降低网络开销和服务响应时间。

### redis 6.X:

    多线程 io Thread
    接收还是epoll单线程，
    之前是接收之后，单线程线性读取数据，比如10个连接，按顺序读数据然后处理，
    现在是接收到多个连接事件之后，开启多个IO线程对每个连接进行read，之后主线程线性处理数据。同理，write也是多线程
    


### 5大类型：
- string:  
    字符串： append
    数值操作：incrby
    bit:   
        统计某用户一年内任意时间窗口的登录情况
        统计一段时间内日活、月活
- list: 双向链表： 为什么能实现数组？
    ltrim：场景：评论列表，第一页评论用缓存
- hash map：
    场景：详情页
- set：无序、去重
    srandmember: 随机返回，场景：批量抽奖
    spop：随即弹出1个，场景：单独抽奖
    sdiff（差集）: 场景：推荐系统
- sorted set: 去重有序集合： 存储格式：双向链表+skiplist(跳表)？
    场景：排行榜
        
#### 其他功能：
1. 发布订阅
2. 三方模块：布隆过滤器 VS 布谷鸟过滤器
3. 秒杀场景：因为单线程，计算向数据移动，decr 剩余

### 过期原理：
    被动和主动方式。
    当一些客户端尝试访问它时，key会被发现并主动的过期。
    当然，这样是不够的，因为有些过期的keys，永远不会访问他们。 无论如何，这些keys应该过期，所以定时随机测试设置keys的过期时间。所有这些过期的keys将会从密钥空间删除。
    具体就是Redis每秒10次做的事情：
    测试随机的20个keys进行相关过期检测。
    删除所有已经过期的keys。
    如果有多于25%的keys过期，重复步奏1.
    这是一个平凡的概率算法，基本上的假设是，我们的样本是这个密钥控件，并且我们不断重复过期检测，直到过期的keys的百分百低于25%,这意味着，在任何给定的时刻，最多会清除1/4的过期keys。


- redis集群 不要在pipeline中使用mget，mset等批量处理key的操作，慎用pipeline。https://help.aliyun.com/document_detail/26356.html
  
  说明:集群实例受限的Redis命令只支持所操作key均分布在单个hash slot中的场景，没有实现多个hash slot数据的合并功能，因此需要用hash tag的方式确保要操作的key均分布在一个hash slot中。

  比如有key1，aakey，abkey3，那么我们在存储的时候需要用{key}1，aa{key}，ab{key}3的方式存储，这样调用受限命令时才能生效。具体关于hash tag的用法请参见Redis官方文档：http://redis.io/topics/cluster-spec。

  事务之前没有使用watch命令且事务中都是单key的命令场景，不再要求所有key必须在同一个slot中，使用方式和直连redis完全一致。其他场景要求事务中所有命令的所有key必须在同一个slot中。

  多key命令包括：DEL、SORT、MGET、MSET、BITOP、EXISTS、MSETNX、RENAME、 RENAMENX、BLPOP、BRPOP、RPOPLPUSH、BRPOPLPUSH、SMOVE、SUNION、SINTER、SDIFF、SUNIONSTORE、SINTERSTORE、SDIFFSTORE、ZUNIONSTORE、ZINTERSTORE、 PFMERGE、PFCOUNT。
  不允许在事务中使用的命令包括：WATCH、UNWATCH、RANDOMKEY、KEYS、SUBSCRIBE、 UNSUBSCRIBE、PSUBSCRIBE、PUNSUBSCRIBE、PUBLISH、PUBSUB、SCRIPT、EVAL、 EVALSHA、SCAN、ISCAN、DBSIZE、ADMINAUTH、AUTH、PING、ECHO、FLUSHDB、 FLUSHALL、MONITOR、IMONITOR、RIMONITOR、INFO、IINFO、RIINFO、CONFIG、 SLOWLOG、TIME、CLIENT。

知识扩展：
```
1.内存：寻址时间：纳秒
2.带宽
epoll
redis集群，卡槽
服务器：
strace
cd /proc/PID
cd task =》线程
视频转码 vep=mp4
IO是什么
fcntl
研究：字节、编码
```
