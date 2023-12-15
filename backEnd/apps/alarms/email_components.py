import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class EmailSender:
    """
    sender_email = '发送者邮箱'
    sender_password = '发送者邮箱密码'
    receivers = ['接收者邮箱', '多个']
    subject = '邮箱标题'
    message_content = '邮箱内容'
    """
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email or '18839970933@163.com'
        self.sender_password = sender_password or 'li824129909322'
        self.smtp_server = 'smtp.163.com'  # 修改为你的SMTP服务器
        self.from_name = "告警BOT"

    def send_email(self, receivers, subject, message_content):
        try:
            smtp_obj = smtplib.SMTP(self.smtp_server)
            smtp_obj.login(user=self.sender_email, password=self.sender_password)

            for receiver in receivers:
                message = MIMEMultipart()
                message['From'] = self.from_name
                message['To'] = receiver
                message['Subject'] = Header(subject, 'utf-8')

                message.attach(MIMEText(message_content, 'plain', 'utf-8'))

                smtp_obj.sendmail(self.sender_email, [receiver], message.as_string())
                print(f"{receiver} 邮件发送成功")

            smtp_obj.quit()
        except smtplib.SMTPException as e:
            print(f"Error: 无法发送邮件，错误明细：{e}")


# 使用示例
if __name__ == "__main__":
    sender_email = ''
    sender_password = ''
    # receivers = ['1025212779@qq.com', 'zio_one@biuloli.tk']
    receivers = ['1025212779@qq.com']
    subject = 'SMTP 邮件测试'
    message_content = '欧耶！邮件发送成功'

    email_sender = EmailSender(sender_email, sender_password)
    email_sender.send_email(receivers, subject, message_content)
