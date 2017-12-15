import psutil
import time
import requests
import json
import os
url = 'https://oapi.dingtalk.com/robot/send?access_token=c6888c8bf3e11cd18063c7aff077753044e051aa7d4d8410106f50cee07c23dc'

#url = 'https://oapi.dingtalk.com/robot/send?access_token=3d94c740a27d5f70da6acf2a1c9383b338ad5c562fbaece8d38595c405e7e6a9'
time_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#当前时间
at_list = []
#需要艾特到的用户列表
monitor_name = {'python3','sshd','httpd'}
#需要监控的服务集合
monitor_map = {'python3':'',
                'sshd':'service ssh start',
                'httpd':'service httpd start',
        }
#定义启动规则

headers = {"Content-Type": "application/json ;charset=utf-8 "}
def send(url,data,headers):
    req = requests.post(url=url,data=send_data,headers=headers)

while True:
    proc_dict = {}
    proc_name = set()
    for p in psutil.process_iter(attrs=['pid','name']):
        proc_dict[p.info['pid']] = p.info['name']
        proc_name.add(p.info['name'])
    proc_stop = monitor_name - proc_name
    if proc_stop:
        print('------------')
        for p in proc_stop:
            p_status = '停止'
            p_name = p
            data = {
                 "msgtype": "markdown",
                 "markdown": {
                     "title":"监控讯息:\n",
                     "text": "#### %s\n" % time_now  +
                             "> ##### 服务名: %s \n\n" % p_name +
                             "> ##### 状态: %s \n" % p_status +
                             "> ##### 正在尝试启动"
                 },
                "at": {
                    "atMobiles": at_list,
                    "isAtAll": True,
                },
            }

            send_data = json.dumps(data).encode('utf-8')
            send(url,send_data,headers)

            os.system(monitor_map[p])
            proc_dict = {}
            proc_name = set()
            for p2 in psutil.process_iter(attrs=['pid','name']):
                proc_dict[p2.info['pid']] = p2.info['name']
                proc_name.add(p2.info['name'])
            #再检查一下这个进程是否存在

            if p in proc_name:
                data = {
                    "msgtype": "markdown",
                    "markdown": {
                            "title":"监控讯息:\n",
                            "text": "#### %s\n" % time_now  +
                            "> ##### 服务名: %s \n\n" % p_name +
                            "> ##### 重启成功"
                     },
                }
                headers = {"Content-Type": "application/json ;charset=utf-8 "}
                send_data = json.dumps(data).encode('utf-8')
                send(url,send_data,headers)

            else:
                data = {
                    "msgtype": "markdown",
                    "markdown": {
                            "title":"监控讯息:\n",
                            "text": "#### %s\n" % time_now  +
                            "> ##### 服务名: %s \n\n" % p_name +
                            "> ##### 重启失败"
                     },
                }
                headers = {"Content-Type": "application/json ;charset=utf-8 "}
                send_data = json.dumps(data).encode('utf-8')
                send(url,send_data,headers)
    time.sleep(2)
