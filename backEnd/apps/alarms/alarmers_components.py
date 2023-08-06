import asyncio

from server_core.db import Newsession
from apps.alarms.models import AlamerJobs, Alamers
from apps.alarms.email_components import EmailSender
from apps.alarms.qw_components import WeChatMessenger


class AlarmHandler:
    def __init__(self):
        self.session = Newsession()

    def handle_alarm(self, wid, subject=None, message_content=None):
        alamer_jobs_data = self.session.query(AlamerJobs).filter_by(wid=wid).all()

        for job_data in alamer_jobs_data:
            aid = job_data.aid
            resource = job_data.resource

            alamer_data = self.session.query(Alamers).filter_by(aid=aid).first()
            if alamer_data and alamer_data.resource == resource:
                if resource == "电子邮件":
                    email_sender = EmailSender(None, None)
                    email_sender.send_email([alamer_data.email], subject, message_content)
                    message = job_data.alarm_content or job_data.desc
                    email_sender.send_email([alamer_data.email], job_data.name, message)
                elif resource == "企微BOT":
                    wechat_messenger = WeChatMessenger(alamer_data.qw_token)
                    message_data = {
                        "msgtype": "text",
                        "text": {"content": job_data.alarm_content or job_data.desc}
                    }
                    asyncio.run(wechat_messenger.send_message(message_data))


# 使用示例
if __name__ == '__main__':
    # alarm_handler = AlarmHandler()
    # alarm_handler.handle_alarm('wid')
    alarm_handler = AlarmHandler()
    alarm_handler.handle_alarm(
        # "a158dc3a9d0f71283132f2c1127bc8c0", "36b64ff8027501145b69ce367b795a87",
        "a158dc3a9d0f71283132f2c1127bc8c0",
        f'xx_有关告警信息',
        f"该任务接收到了一次报错日志！内容如下:"
        f"测试！"
    )
