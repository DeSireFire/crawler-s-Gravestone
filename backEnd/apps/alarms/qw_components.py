import asyncio
import httpx


class WeChatMessenger:
    def __init__(self, qw):
        self.webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={qw}"

    async def send_message(self, message_data):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url=self.webhook_url, headers=headers, json=message_data)
            assert resp.status_code == 200
            return resp.text


if __name__ == '__main__':
    description = [
        "机器人推送测试",
    ]
    data = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "药物临床试验登记与信息公示平台",
                    "description": "\n".join(description),
                    "url": "http://www.chinadrugtrials.org.cn/index.html",
                    "picurl": "http://www.chinadrugtrials.org.cn/website/img/bodybg3.jpg"
                }
            ]
        }
    }

    qw = "542e14c0-db35-4f3b-9f8b-850ecafb1b8c"
    # qw = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=542e14c0-db35-4f3b-9f8b-850ecafb1b8c"

    messenger = WeChatMessenger(qw)
    response = asyncio.run(messenger.send_message(data))
    print(response)
