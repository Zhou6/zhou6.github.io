## docker容器基本使用
- docker info    # 查看docker信息
- docker run -i -t ubuntu /bin/bash   # 使用ubuntu镜像创建新容器，并执行/bin/bash命令，且进行交互
- docker ps -a    # 查看所有已有容器，不带-a则只展示正在进行等起
- docker ps -n 10    # 展示最后10个容器，无论状态
- docker --name my_container -i -t ubuntu /bin/bash    # 创建守护式新容器并命名
- docker start my_container    # 启动my_container容器，但并没有交互， my_container也可以替换为容器唯一id
- docker attach my_container    # 附着到已启动的my_container容器，可以进行交互
- docker run --name daemon_z -d ubuntu /bin/sh -c "while true;do echo hello;sleep 5;done"    # 使用ubuntu镜像创建并在后台运行daemon_z容器，并执行脚本
- docker logs daemon_z    # 查看daemon_z容器log
  - docker logs -f daemon_z    # 类似tail -f
  - docker logs --tail 10 -f daemon_z    # 类似tail -f log -n 10
- docker top daemon_z    # 类似top查看daemon_z容器进程
- docker exec -d daemon_z touch /etc/new_config_file    # 在daemon_z中以后台任务形式执行创建new_config_file文件命令，
  - docker exec：向容器传送命令， 
  - -d：后台任务
- docker exec -t -i daemon_z /bin/bash    # 在daemon_z执行创建新的bash会话命令
- docker stop daemon_z    # 停止容器
- docker run --restart=always --name daemon_restart -d ubuntu /bin/sh -c "while true;do echo hello;sleep 5;done"
  - --restart:自动重启  
    - always：无论什么情况都会重启  
    - on-failure：只有容器退出代码为非0会重启，on-failure还可接受重启次数参数  --restart=on-failure:5
- docker inspect daemon_restart  # daemon_restart容器相关信息
- docker rm daemon_restart  # 删除容器
  - docker rm ‘docker ps -a -q’  # 删除所有容器
  
## docker镜像
