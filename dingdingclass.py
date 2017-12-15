# coding: utf-8
import time
import os
import requests
import json
import psutil


class alarmhandler(object):
    def __init__(self):
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=80ab5cb49bb8b09ed1d5119289ea651461546b7670caffb75a98e3384f81d007"
        self.headers = {"Content-Type": "application/json;charset: utf-8"}
        self.monitor_name = {'python'}  # 定义监控服务
        self.monitor_map = {'python': 'python /data/deploy_flann/server.py &'}
        self.time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.sendDate = None

    def run(self, url, data, headers):
        req = requests.post(url=self.url, data=self.sendData, headers=self.headers)
        print(req)

    def isRunning(self):  # 检查进程是否存在
        proc_dict = {}  # 创建一个进程id和进程名对应的字典
        proc_name = set()  # 集合用来保存当前系统开启的进程名
        for p in psutil.process_iter(attrs=['pid', 'name']):
            proc_dict[p.info['pid']] = p.info['name']
            proc_name.add(p.info['name'])  # 集合
        proc_stop = self.monitor_name - proc_name  # 集合差补
        if proc_stop:
            print('----------------------')
            for p in proc_stop:
                p_status = '停止'
                p_name = p
                data_info = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": "监控信息：\n",
                        "text": "#### %s \n" % self.time_now +
                                "> #### 服务名： %s \n\n" % p_name +
                                "> ##### 状态: %s \n" % p_status +
                                "> #### 正在尝试重新启动"
                    },
                    "at": {
                        "isAtAll": True,
                    },
                }
                self.sendData = json.dumps(data_info).encode('utf-8')
                self.run(self.url, self.sendData, self.headers)
                os.system(self.monitor_map[p])  # 启动进程
                proc_dict = {}
                proc_name = set()
                for p2 in psutil.process_iter(attrs=['pid', 'name']):  # 再次检查进程是否存在
                    proc_dict[p2.info['pid']] = p2.info['name']
                    proc_name.add(p2.info['name'])
                    if p in proc_name:
                        data_info = {
                            "msgtype": "markdown",
                            "markdown": {
                                "title": "监控信息：\n",
                                "text": "#### %s \n" % self.time_now +
                                        "> #### 服务名： %s \n\n" % p_name +
                                        "> #### 重启成功"
                            },
                            "at": {
                                "isAtAll": True
                            },
                        }
                        self.sendData = json.dumps(data_info).encode('utf-8')
                        self.run(self.url, sendData, self.headers)
                    else:
                        data_info = {
                            "msgtype": "markdown",
                            "markdown": {
                                "title": "监控讯息:\n",
                                "text": "#### %s\n" % self.time_now +
                                        "> ##### 服务名: %s \n\n" % p_name +
                                        "> ##### 重启失败"
                            },
                            "at": {
                                "isAtAll": True
                            },
                        }
                        self.sendData = json.dumps(data_info).encode('utf-8')
                        self.run(self.url, self.sendData, self.headers)
                        break
        else:
            data_info = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "监控讯息:\n",
                    "text": "#### %s\n" % self.time_now +
                            "> ##### 服务器运行正常"
                },
                "at": {
                    "isAtAll": True
                },
            }
            self.sendData = json.dumps(data_info).encode('utf-8')
            self.run(self.url, self.sendData, self.headers)


if __name__ == '__main__':
    vc = alarmhandler()
    vc.isRunning()
