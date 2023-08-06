import asyncio
import time
import httpx

def card_tel(title:str,
            description:list,
            url:str,
            picurl:str):
    """
    快速推送信息卡片导企业微信
    :param title: 标题
    :param description: list, 推送描述，列表一个元素是一行
    :param url: 跳转到url
    :param picurl: 卡片展示用的图片url
    :return:
    """
    cb = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": title,
                    "description": "\n".join(description),
                    "url": url,
                    "picurl": picurl
                }
            ]
        }
    }
    CLS = FicTelegraph(cb)
    CLS.telegraph()

class FicTelegraph(object):
    """
    创新药采集报文推送机器人
    description = [
        "CTR 全量采集",
        "",
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
    """

    def __init__(self, callback_info=None):
        if callback_info is None:
            callback_info = {}
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=542e14c0-db35-4f3b-9f8b-850ecafb1b8c"

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }

        self.callback_info = callback_info

    def telegraph(self):
        if self.callback_info:
            asyncio.run(self.main())
        else:
            print(f"没有传入需要发送的信息，请将发送内容传入FicTelegraph.callback_info变量！json格式参看类描述或企微机器人文档")

    async def make_request(self):
        async with httpx.AsyncClient() as client:
            resp = await client.post(url=self.url, headers=self.headers, json=self.callback_info)
            assert resp.status_code == 200
            html = resp.text
            print(html)

    async def main(self):
        tasks = [asyncio.create_task(self.make_request()) for _ in range(1)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    description = [
        "CTR 全量采集",

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
    data2 = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "news_notice",
            "source": {
                "icon_url": "https://wework.qpic.cn/wwpic/252813_jOfDHtcISzuodLa_1629280209/0",
                "desc": "企业微信",
                "desc_color": 0
            },
            "main_title": {
                "title": "欢迎使用企业微信",
                "desc": "您的好友正在邀请您加入企业微信"
            },
            "card_image": {
                "url": "https://wework.qpic.cn/wwpic/354393_4zpkKXd7SrGMvfg_1629280616/0",
                "aspect_ratio": 2.25
            },
            "image_text_area": {
                "type": 1,
                "url": "https://work.weixin.qq.com",
                "title": "欢迎使用企业微信",
                "desc": "您的好友正在邀请您加入企业微信",
                "image_url": "https://wework.qpic.cn/wwpic/354393_4zpkKXd7SrGMvfg_1629280616/0"
            },
            "quote_area": {
                "type": 1,
                "url": "https://work.weixin.qq.com/?from=openApi",
                "appid": "APPID",
                "pagepath": "PAGEPATH",
                "title": "引用文本标题",
                "quote_text": "Jack：企业微信真的很好用~\nBalian：超级好的一款软件！"
            },
            "vertical_content_list": [
                {
                    "title": "惊喜红包等你来拿",
                    "desc": "下载企业微信还能抢红包！"
                }
            ],
            "horizontal_content_list": [
                {
                    "keyname": "邀请人",
                    "value": "张三"
                },
                {
                    "keyname": "企微官网",
                    "value": "点击访问",
                    "type": 1,
                    "url": "https://work.weixin.qq.com/?from=openApi"
                },
                {
                    "keyname": "企微下载",
                    "value": "企业微信.apk",
                    "type": 2,
                    "media_id": "MEDIAID"
                }
            ],
            "jump_list": [
                {
                    "type": 1,
                    "url": "https://work.weixin.qq.com/?from=openApi",
                    "title": "企业微信官网"
                },
                {
                    "type": 2,
                    "appid": "APPID",
                    "pagepath": "PAGEPATH",
                    "title": "跳转小程序"
                }
            ],
            "card_action": {
                "type": 1,
                "url": "https://work.weixin.qq.com/?from=openApi",
                "appid": "APPID",
                "pagepath": "PAGEPATH"
            }
        }
    }
    CLS = FicTelegraph(data)
    CLS.telegraph()
