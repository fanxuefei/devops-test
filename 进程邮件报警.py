#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#进程失效邮件报警脚本
import os,time
import smtplib
import datetime
from email.mime.text import MIMEText
#设置邮件发送
mailto_list=['fanxuefei@aicyber.com']#收件人邮箱
mail_host="smtp.qq.com"#发件人邮箱服务器
mail_user="22380425"#发件人邮箱用户名
mail_pass="dgsjeznmvdlabhda"#发件人邮箱密码
mail_postfix="qq.com"#发件人邮箱后缀
def send_mail(to_list,sub,content):#to_list：收件人；sub：主题；content：邮件内容
    me="服务器报告"+"<"+mail_user+"@"+mail_postfix+">" 
    msg = MIMEText(content,_subtype='html',_charset='gb2312') #创建一个实例，这里设置为html格式邮件
    msg['Subject']=sub
    msg['From'] = me
    msg['To'] =",".join(to_list)#将收件人列表以,分隔
    try:  
        server = smtplib.SMTP_SSL("smtp.qq.com",465)  
        server.connect(mail_host)                       #连接服务器  
        server.login(mail_user,mail_pass)               #登录操作  
        server.sendmail(me, to_list, msg.as_string())   #发送邮件
        server.close()  
        return True  
    except Exception as e:
        print(str(e))
        return False  
def log(logfile,content):  #定义日志函数
    f = open(logfile,'a')
    f.write(time.strftime("\n%Y-%m-%d %H:%M:%S   ") + content)
    f.flush()
    f.close()
def isRunning(process_name): #检查进程是否存在，存在为True，不存在为False
    try:
        process = len(os.popen('ps axu | grep "' + process_name + '" | grep -v grep | grep root ').readlines())
        if process >= 1:
            return True
        else:
            return False
    except:
        print("Chect process ERROR!!!")
        return False
def startProcess(process_script):#启动进程脚本，启动成功返回0，不成功返回其他为False
    try:
        result_code = os.system(process_script)
        if result_code == 0 :
            return True
        else:
            return False
    except:
        print("Process start Error!!!")
        return False
with open(r"/home/ubuntu/configfile.txt","r") as f:
    process_list = f.readlines()
if __name__ == '__main__':
    logfile = "/home/ubuntu/logs/logfile.log"  # 定义日志目录
    content = ""  # 定义日志需要填写的内容
    with open(logfile, 'a') as f:
        f.write('-----------------------------------------\n')
    for process in process_list:
        process_name = process.split(":")[0].strip()#定义进程名称
        process_script = process.split(":")[1].strip()#定义启动脚本
        isrunning = isRunning(process_name)  # 运行检查进程
        if isrunning == False:  # 如果进程不存在
            content = process_name + "     ERROR \n" # 把这条字符串追加到log日志文件
            log(logfile, content) # 写入日志
            start_time = datetime.datetime
            send_mail(mailto_list,"%s 进程崩溃 " % process_name,"uwsgi_web 服务器  %s 进程崩溃，请速与管理员联系" % start_time) #发送报警邮件
            print("第一次发送邮件")
            isstart = startProcess(process_script)  # 执行启动脚本函数，接收最后的返回值
            print(isstart)
            if isstart == True:  # 如果返回值是True，进程重启成功
                content += process_name + "   restart  SUCCESS \n"  # 追加这条字符串到日志
                log(logfile, content)  # 写入日志
                send_mail(mailto_list,"SUCCESS","进程重启成功") #发送报警邮件
                print("第二次发送邮件")
        else:
            content = process_name +  "    running \n"
            log(logfile, content)



