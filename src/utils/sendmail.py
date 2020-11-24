#!/usr/bin/python
# coding:utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


class Email:
    def __init__(self, to_list, sub, content):
        '''
        to_list:发给谁
        sub:主题
        content:内容
        send_mail("aaa@126.com","sub","content")
        '''
        #####################
        # 设置服务器，用户名、口令以及邮箱的后缀
        self.to_list = to_list
        self.mail_host = 'smtp.exmail.qq.com'
        self.mail_user = 'report'
        self.mail_postfix = 'xxx.com'

        self.me = self.mail_user + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        # 尝试用utf8和GBK解码邮件内容和主题成unicode
        try:
            content = unicode(content, 'utf8')
            sub = unicode(sub, 'utf8')
        except UnicodeDecodeError:
            try:
                content = unicode(content, 'gbk')
                sub = unicode(sub, 'gbk')
            except UnicodeDecodeError:
                # print format_exc()
                return False
        # 已经是unicode
        except TypeError:
            pass

        self.msg = MIMEMultipart('related')
        self.msg['Subject'] = sub
        self.msg['From'] = 'report@xxx.com'  # report用户没有可以建一个或者用已注册的其他的
        self.msg['To'] = ";".join(to_list)

        txt = MIMEText(content.encode('utf-8'), 'html', 'UTF-8')
        self.msg.attach(txt)

    def add_image(self, file_name):

        # prefix = file_name.split('.')[0]
        image = MIMEImage(open(file_name, 'rb').read())
        end_index = file_name.rfind('/')
        if end_index != -1:
            tag = file_name[end_index + 1:]
        else:
            tag = file_name
        tag = tag.split('.')[0]
        image.add_header('Content-ID', '<' + tag + '>')
        # image.add_header("Content-Disposition", "inline", filename=file_name)
        # image.add_header('Content-Disposition', 'attachment', filename=file_name)

        self.msg.attach(image)

    def send_mail(self):
        try:
            s = smtplib.SMTP()
            s.connect(self.mail_host, 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            # s.set_debuglevel(1)
            s.login('report@xxx.com', '***')  # ***为密码

            s.sendmail(self.me, self.to_list, self.msg.as_string())
            s.close()
            return True
        except Exception, e:
            print e
            # print format_exc()
            return False


def get_tag_name(pic_name):
    end_index = pic_name.rfind('/')
    if end_index != -1:
        tag = pic_name[end_index + 1:]
    else:
        tag = pic_name
    return tag


def send_mail(mail_list, sub, content, images=None):
    email_sender = Email(mail_list, sub, content)
    if images:
        for image in images:
            email_sender.add_image(image)
    email_sender.send_mail()


if __name__ == "__main__":
    mail_list = ['shilu.dong@yingzt.com']
    sub = ""
    pic_name = "pystore/data_pic/test_pic.png"
    # pic_name2 = "/home/work/dongshilu/workspace/report_log/daily_log/20130921-swux-CDN.png"

    pic_tag1 = get_tag_name(pic_name)
    # pic_tag2 = get_tag_name(pic_name2)

    content = '<img src="cid:%s">' % (pic_tag1)

    email_sender = Email(mail_list, sub, content)

    email_sender.add_image(pic_name)
    # email_sender.add_image(pic_name2) 

    email_sender.send_mail()
