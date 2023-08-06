import asyncio
import httpx


class WeChatMessenger:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    async def send_message(self, message_data):
        headers = {
            'Content-Type': 'application/json',
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url=self.webhook_url, headers=headers, json=message_data)
            assert resp.status_code == 200
            return resp.text


if __name__ == '__main__':
    description = [
        "CTR 全量采集 开发测试",
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

    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_webhook_key"

    messenger = WeChatMessenger(webhook_url)
    response = asyncio.run(messenger.send_message(data))
    print(response)
