## mongodb
- 副本集：Primary主节点用来写，Secondary用来读
- 分片集群：一个数据表的数据分成几片分布在不同服务器上，适合连续数据的查找
- 分片的基础上还可以配置副本集
### 本地mongo加用户权限
* kill mongo进程

      ps aux|grep mongo
      kill mongo_pid
*  之后运行无验证版mongo
            
       /usr/local/mongodb/bin/mongod -dbpath /data/db/ -logpath /data/db/mongo.log -logappend -fork -port 27017
*  然后连接mongo，去对应db创建用户
       
       use base_db
       db.createUser({user:"shop_a", pwd:"shop123", roles: [ { role: "dbOwner", db: "base_db" } ]})
*  成功之后，退出mongo
       
       ps aux|grep mongo
       kill mongo_pid
*  之后运行有验证版mongo
                
       /usr/local/mongodb/bin/mongod -dbpath /data/db/ -logpath /data/db/mongo.log -logappend -fork -port 27017 --auth
