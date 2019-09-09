## linux基本命令

#### 连mongo数据库:
    /home/ubuntu/tmp/mongodb-linux-x86_64-ubuntu1404-3.0.9/bin/mongo <my_host>:<my_port>/<db_name> -u <user_name> -p <user_pwd>
#### 后台开端口
    ps aux | grep 10070
    nohup /home/virtenv/bin/python api.py 10070 &
#### Nginx
    sudo nginx -t # 测试
    sudo nginx -s reload
#### supervisor
    sudo supervisorctl reload
    tail -f /backup/logs/supervisor/l_api_out.log
#### crontab
    sudo crontab -e
#### vim
- 查找  
         
      :/search_word   回车   n:下一个   shift+n:上一个
- 替换   
        
      :%s/old/new/g
#### 查看Auth.log,检查SSH是否被扫
- 查看用密码登陆成功的IP地址及次数
    
      grep "Accepted password for root" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr | more
- 查看用密码登陆失败的IP地址及次数

      grep "Failed password for root" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr | more

#### rtmp直播流合并成视频文件

      rtmpdump -v -r rtmp://vba05ca49.live.126.net/live/39909b31438e4e03b8ec5420fcaf1a05

#### 查看某一端口  
    lsof -i:8060
#### 查看端口使用情况
    netstat
#### 查看进程的status文件
     cat /proc/PID/status
#### 搜索包
    apt-cache search ‘package’
#### 创建虚拟环境并指定PYTHON版本
    virtualenv venv --python=python3.6
#### 批量kill pid
    ps -ef|grep 'Split'|grep -v grep| awk '{print $2}'|xargs kill -9

