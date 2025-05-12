import base64
import sys
import time
import json
import requests
import re
sys.path.append('..')
from base.spider import Spider
from bs4 import BeautifulSoup

class Spider(Spider):
    def getName(self):
        return "Litv"

    def init(self, extend):
        self.extend = extend
        try:
            self.extendDict = json.loads(extend)
        except:
            self.extendDict = {}

        proxy = self.extendDict.get('proxy', None)
        if proxy is None:
            self.is_proxy = False
        else:
            self.proxy = proxy
            self.is_proxy = True
        pass

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def natural_sort_key(self, s):
        """
        自然排序辅助函数
        """
        return [
            int(part) if part.isdigit() else part.lower()
            for part in re.split(r'(\d+)', s)
        ]

    def liveContent(self, url):
        m3u_content = ['#EXTM3U']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Referer': 'https://360pai.xyz/',
        }

        try:
            response = requests.get('https://360pai.xyz/live', headers=headers, timeout=10)
            response.raise_for_status()
            res = response.text
            soup = BeautifulSoup(res, 'html.parser')
            result = []
            
            cards = soup.select('div.anchor-grid_anchor-card-wrap__NR9Ov')
            exif = f'#EXTINF:-1 tvg-name="by公众号[医工学习日志]" group-title="360pai",by公众号[医工学习日志]'
            m3u_content.extend([exif, "by公众号[医工学习日志]"])
            for card in cards:
                a_tag = card.find('a', class_='anchor-grid_anchor-card__nJf0J')
                if not a_tag:
                    continue
                
                href = a_tag.get('href', '')
                live_id_match = re.search(r'/live/([^/]+)', href)
                if not live_id_match:
                    continue
                live_id = live_id_match.group(1)
                
                title_div = a_tag.find('div', class_='anchor-grid_anchor-avatar-title__5hTsp')
                title = title_div.get_text(strip=True) if title_div else ''
                title = title.replace(" vs ","vs")
                if not title:
                    continue
                
                extinf = f'#EXTINF:-1 tvg-name="{title}" group-title="360pai",{title}'
                ch_url = f"video://https://360pai.xyz/live/{live_id}"
                
                m3u_content.extend([extinf, ch_url])
                #print(m3u_content)
            
        except requests.exceptions.RequestException as e:
            print(f"网络请求失败: {e}")
        except Exception as e:
            print(f"处理过程中发生错误: {e}")
        return '\n'.join(m3u_content)
        
        

    def homeContent(self, filter):
        return {}

    def homeVideoContent(self):
        return {}

    def categoryContent(self, cid, page, filter, ext):
        return {}

    def detailContent(self, did):
        return {}

    def searchContent(self, key, quick, page='1'):
        return {}

    def searchContentPage(self, keywords, quick, page):
        return {}

    def playerContent(self, flag, pid, vipFlags):
        return {}

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        if params['type'] == "ts":
            return self.get_ts(params)
        return [302, "text/plain", None, {'Location': 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'}]
    def proxyM3u8(self, params):
        pid = params['pid']
        info = pid.split(',')
        a = info[0]
        b = info[1]
        c = info[2]
        timestamp = int(time.time() / 4 - 355017625)
        t = timestamp * 4
        m3u8_text = f'#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:4\n#EXT-X-MEDIA-SEQUENCE:{timestamp}\n'
        for i in range(10):
            url = f'https://ntd-tgc.cdn.hinet.net/live/pool/{a}/litv-pc/{a}-avc1_6000000={b}-mp4a_134000_zho={c}-begin={t}0000000-dur=40000000-seq={timestamp}.ts'
            if self.is_proxy:
                url = f'http://127.0.0.1:9978/proxy?do=py&type=ts&url={self.b64encode(url)}'

            m3u8_text += f'#EXTINF:4,\n{url}\n'
            timestamp += 1
            t += 4
        return [200, "application/vnd.apple.mpegurl", m3u8_text]


    def get_ts(self, params):
        url = self.b64decode(params['url'])
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, stream=True, proxies=self.proxy)
        return [206, "application/octet-stream", response.content]

    def destroy(self):
        return '正在Destroy'

    def b64encode(self, data):
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    def b64decode(self, data):
        return base64.b64decode(data.encode('utf-8')).decode('utf-8')


if __name__ == '__main__':
    pass
