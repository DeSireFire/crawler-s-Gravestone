import asyncio

from server_core.db import Newsession
from apps.alarms.models import AlamerJobs, Alamers
from apps.alarms.email_components import EmailSender
from apps.alarms.qw_components import WeChatMessenger
from server_core.log import logger

class AlarmHandler:
    def __init__(self):
        self.session = Newsession()
        self.receivers = []

    async def handle_alarm(self, wid, subject=None, message_content=None):
        # 筛选出wid符合且状态为开启的监控任务
        alamer_jobs_data = self.session.query(AlamerJobs).filter_by(wid=wid, delivery=1).all()

        for job_data in alamer_jobs_data:
            aid = job_data.aid
            resource = job_data.resource

            alamer_data = self.session.query(Alamers).filter_by(aid=aid).first()
            if alamer_data and alamer_data.resource == resource:
                if resource == "电子邮件":
                    email_sender = EmailSender(None, None)
                    email_sender.send_email([alamer_data.email], subject, message_content)

                if resource == '企微bot':
                    wechat_messenger = WeChatMessenger(alamer_data.qw_token)
                    description = [subject]
                    if isinstance(message_content, str):
                        description.append(message_content)
                    if isinstance(message_content, list):
                        description += message_content
                    message_data = {
                        "msgtype": "news",
                        "news": {
                            "articles": [
                                {
                                    "title": f"平台报警信息",
                                    "description": "\n".join(description),
                                    "url": "https://www.sinohealth.cn",
                                    "picurl": "http://www.chinadrugtrials.org.cn/website/img/bodybg3.jpg"
                                }
                            ]
                        }
                    }
                    task = asyncio.create_task(
                        wechat_messenger.send_message(message_data)
                    )
                    push_response = await task
                    if 'ok' not in push_response:
                        logger.error(
                            f"推送企业微信机器人信息时，发生了错误：{push_response}"
                        )


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
