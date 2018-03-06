#!coding:utf8
"""
通知的一些信息
"""
from dtlib.dtlog import dlog
import string
import smtplib


class MailMsg(object):
    """
    邮件对象
    """

    def __init__(self):
        self.smtp = "smtp.qq.com"
        self.account = '1490@qq.com'
        self.psw = 'xxxxxx'

        self.from_mail = self.account
        self.to_mail = "aa@qq.com"
        self.mail_title = "[e-notice]:default-mail-title"
        self.mail_body = 'default-mail-body'

    def set_title(self, mail_title='email-notice'):
        self.mail_title = mail_title

    def set_body(self, mail_body='noteice-body'):
        self.mail_body = mail_body

    def set_to_mail(self, to_mail=''):
        self.to_mail = to_mail

    def send(self):
        """
        发送邮件,title,body
        """
        server = smtplib.SMTP(self.smtp)
        server.login(self.account, self.psw)

        mail_content = string.join((
            "From: %s" % self.from_mail,
            "To: %s" % self.to_mail,
            "Subject: %s" % self.mail_title,
            "",
            self.mail_body), "\r\n")

        server.sendmail(self.from_mail, [self.to_mail], mail_content)
        server.close()


if __name__ == '__main__':
    dlog.debug('run in main')

    mail = MailMsg()
    mail.send()
    dlog.debug('finished in main')
