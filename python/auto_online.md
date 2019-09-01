## 自动上线脚本
- 调用online.py脚本，调用线上接口
```
#!/usr/bin/env python
# coding=utf-8

# pip install aliyun-python-sdk-slb
# pip install aliyun-python-sdk-ecs
import json
import sys

import requests
import time

from aliyunsdkcore.client import AcsClient
from aliyunsdkslb.request.v20140515.SetBackendServersRequest import SetBackendServersRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import DescribeLoadBalancerAttributeRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

ONLINE_URL = 'http://%s/base/online'
URL = 'www.my.com'


class OnlineTool(object):

    def __init__(self, access_key_id, access_key_secret, load_balancer_id=None, region_id='cn-beijing'):
        self.client = AcsClient(access_key_id, access_key_secret, region_id)
        self.load_balancer_id = load_balancer_id

    def set_server_weight(self, server_id, weight, server_type='ecs'):
        """配置权重"""
        request = SetBackendServersRequest()
        request.set_accept_format('json')

        request.set_BackendServers(
            "[{\"Type\":\"%s\",\"ServerId\":\"%s\",\"Weight\":\"%s\"}]" % (server_type, server_id, weight))
        request.set_LoadBalancerId(self.load_balancer_id)

        response = self.client.do_action_with_exception(request)
        return response

    def get_load_banlancer_detail(self):
        """获取负载均衡实例详细信息"""
        request = DescribeLoadBalancerAttributeRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(self.load_balancer_id)
        response = self.client.do_action_with_exception(request)
        return response

    def get_servers_weight(self):
        """获取服务器权重"""
        response = self.get_load_banlancer_detail()
        backend_servers = json.loads(response).get('BackendServers').get('BackendServer')
        servers_dict = {}
        for server in backend_servers:
            servers_dict[server.get('ServerId')] = server.get('Weight')
        return servers_dict

    def get_server_detail(self, instance_id=None, instance_ids=None):
        """获取服务器详细信息"""
        if instance_id:
            instance_ids = [instance_id]
        request = DescribeInstancesRequest()
        request.set_accept_format('json')

        if instance_ids:
            request.set_InstanceIds(json.dumps(instance_ids))
        response = self.client.do_action_with_exception(request)
        instances = json.loads(response).get('Instances').get('Instance')
        return instances[0] if instance_id else instances


def online_servers(access_key_id, access_key_secret, branch='master', task='all',
                   no_need_online_servers=None):
    """线上服务器上线"""
    try:
        online_tool = OnlineTool(access_key_id, access_key_secret, load_balancer_id='lb-2zeggz2ft6sqnprujskzk')
        servers_dict = {}
        result = online_tool.get_servers_weight()
        ips = result.keys()
        details = online_tool.get_server_detail(instance_ids=ips)
        for detail in details:
            private_ip = detail.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0]
            InstanceId = detail.get('InstanceId')
            InstanceName = detail.get('InstanceName')
            servers_dict[InstanceName] = {'InstanceId': InstanceId, 'private_ip': private_ip,
                                          'weight': result.get(InstanceId)}

        if no_need_online_servers and isinstance(no_need_online_servers, list):
            for no_need_online_server in no_need_online_servers:
                servers_dict.pop(no_need_online_server)  # 不需要上线的机器

        for k, v in servers_dict.iteritems():
            print '==================== %s BEGIN %s ====================' % (k, int(time.time()))
            print '========== %s SET_WEIGHT %s ==========' % (k, 0)
            # 设置权重为0
            result = online_tool.set_server_weight(v.get('InstanceId'), 0)
            print result
            time.sleep(3)

            result = online(v.get('private_ip'), branch, task)
            if result != 0:
                print k, 'online ERROR'
                return
            time.sleep(3)
            print k, '========== SET_WEIGHT %s ==========' % v.get('weight')
            # 恢复权重
            result = online_tool.set_server_weight(v.get('InstanceId'), v.get('weight'))
            print result
            print '==================== %s SUCCESS END %s ====================' % (k, int(time.time()))
    except Exception as e:
        print 'EXCEPTION', e.message


def test_server(ip=URL, branch='master', task='all'):
    """测服上线"""
    ret = online(ip, branch, task)


def online(ip, branch='master', task='all'):
    """调接口，执行拉代码、重启服务等操作"""
    print '=============== %s online BEGIN %s ===============' % (ip, time.time())
    ret = requests.post(ONLINE_URL % ip, json={'branch': branch, 'task': task})
    print '========== return data BEGIN =========='
    if ret.status_code != 200:
        print 'status_code', ret.status_code
        print 'ERROR END'
        return -1

    if ret.json().get('code') != 1:
        print 'error_msg', ret.json()
        print 'ERROR END'
        return -1
    data = ret.json().get('data')
    outputs = json.loads(data.get('output'))
    for output in outputs:
        print output
    print '========== return data END =========='

    time.sleep(4)  # 等待supervisor重启
    while True:
        # 检查服务是否已经重启完成
        ret = requests.post(ONLINE_URL % ip, json={'test': 'True'})
        if ret.status_code == 200:
            print '========== return test data BEGIN =========='
            if ret.json().get('code') != 1:
                print 'error_msg', ret.json()
                print 'ERROR END'
                return -1
            data = ret.json().get('data')
            outputs = json.loads(data.get('output'))
            for output in outputs:
                print output
            print '========== return test data END =========='
            break
        else:
            print 'status_code = ', ret.status_code
            print 'sleep 1'
            time.sleep(1)
    print '=============== %s online END %s ===============' % (ip, time.time())
    return 0


if __name__ == '__main__':
    # 去自己aliyun账号里新建一个access_key，获取access_key_id，access_key_secret
    access_key_id = sys.argv[1] if len(sys.argv) >= 2 else ''
    access_key_secret = sys.argv[2] if len(sys.argv) >= 3 else ''
    # online_servers(access_key_id, access_key_secret)
    test_server(branch='zqm', task='my_task')

```
- 线上接口代码
```
base_view = Blueprint('base', __name__, url_prefix='/base')
@base_view.route("/online", methods=["POST"])
def online():
    ip = request.headers.get('X-Real-Ip')
    if ip not in ACCESS_IPS:
        return render_response(RetCodeAndMessage.Illegal_Operation)
    test = request.all_param.get("test", "")
    if test:
        cmd_list = ['cd ..',
                    'pwd',
                    'git log -1']
        result = ['ip: ' + ip]
        for cmd in cmd_list:
            output = commands.getoutput(cmd)
            result.append(cmd)
            result.append(output)
        return render_response(RetCodeAndMessage.Success, data={'output': json.dumps(result)})
    task = request.all_param.get("task", "")
    branch = request.all_param.get("branch", "")
    if not task or not branch:
        return render_response(RetCodeAndMessage.Illegal_Operation)
    cmd_list = ['cd ..',
                'pwd',
                'git stash',
                'git checkout %s' % branch,
                'git pull']
    result = ['ip: ' + ip]
    for cmd in cmd_list:
        output = commands.getoutput(cmd)
        result.append(cmd)
        result.append(output)
    thrd = threading.Timer(3.0, supervisor_restart, args=[task])
    thrd.start()
    return render_response(RetCodeAndMessage.Success, data={'output': json.dumps(result)})

def supervisor_restart(task):
    # 为了先return data，后重启服务，所以开了线程等待3秒后，再执行。
    # python进程结束之后，subprocess.Popen里执行的进程并不会随之结束，其他写法会随之结束，不知道为什么，待查询
    with open(os.devnull, 'r+b', 0) as DEVNULL:
        subprocess.Popen('nohup %s &' % ('supervisorctl restart %s' % task), shell=True, stdout=DEVNULL, stderr=DEVNULL)
```

