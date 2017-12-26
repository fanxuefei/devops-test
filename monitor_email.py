import smtplib
from email.mime.text import MIMEText
#设置邮件发送
class mail_send(object):
    def __init__(self):
        self.mailto_list=['fanxuefei@aicyber.com']#收件人邮箱
        self.mail_host="smtp.exmail.qq.com"#发件人邮箱服务器
        self.mail_user="monitor"#发件人邮箱用户名
        self.mail_pass="ubuntu330M"#发件人邮箱密码
        self.mail_postfix="aicyber.com"#发件人邮箱后缀

    def send_mail(self,sub,content):#to_list：收件人；sub：主题；content：邮件内容
        me="服务器报告"+"<" + "python text" + ">"
        msg = MIMEText(content,_subtype='html',_charset='gb2312') #创建一个实例，这里设置为html格式邮件
        msg['Subject']=sub
        msg['From'] = me
        msg['To'] =",".join(self.mailto_list)#将收件人列表以,分隔
        try:
            server = smtplib.SMTP(self.mail_host,25)
            server.connect(mail_host)                       #连接服务器
            server.login(mail_user,mail_pass)               #登录操作
            server.sendmail(me, self.mailto_list, msg.as_string())   #发送邮件
            server.close()
            return True
        except Exception as e:
            print(str(e))
            return False


vc = mail_send()
vc.send_mail()