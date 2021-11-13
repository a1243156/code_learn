import time
import threading
import requests
import queue

t1 = time.time()

url = 'https://user-worker-api.wanshifu.com/master/listInfo'

headers = {}
headers['Accept'] = 'application/json, text/plain, */*'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
headers['Connection'] = 'keep-alive'
headers['Content-Length'] = '62'
headers['Content-Type'] = 'application/x-www-form-urlencoded'
headers['Cookie'] = 'gr_user_id=ceeb087b-cf1a-49da-9320-fe2f87af9a40; 8d8663ae5baca813_gr_last_sent_cs1=%20; 8d8663ae5baca813_gr_session_id=d6441883-1ad8-45a1-9149-1e424c4a5a2b; 8d8663ae5baca813_gr_last_sent_sid_with_cs1=d6441883-1ad8-45a1-9149-1e424c4a5a2b; 8d8663ae5baca813_gr_session_id_d6441883-1ad8-45a1-9149-1e424c4a5a2b=true; hotline_id=; acw_tc=2f6a1fb116364266418865349e4713e8bd2ff0fef0ba83f1862c1e00f24ff7; Hm_lvt_e74f5753a090f5adb8cc7ee84fb3b3a1=1636014656,1636426622,1636428268; 8d8663ae5baca813_gr_cs1=%20; Hm_lpvt_e74f5753a090f5adb8cc7ee84fb3b3a1=1636428274'
headers['Host'] = 'user-worker-api.wanshifu.com'
headers['Origin'] = 'https://worker.wanshifu.com'
headers['Referer'] = 'https://worker.wanshifu.com/'
headers['sec-ch-ua'] = '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"'
headers['sec-ch-ua-mobile'] = '?0'
headers['sec-ch-ua-platform'] = '"Windows"'
headers['Sec-Fetch-Dest'] = 'empty'
headers['Sec-Fetch-Mode'] = 'cors'
headers['Sec-Fetch-Site'] = 'same-site'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

date = {}
date['userCategoryId'] = '1'
date['categoryName'] = 'jiaju'
date['pageNum'] = '2'
date['categoryId'] = 'jiaju'

class MyThread(threading.Thread):

    """自定义一个多线程类"""

    def __init__(self,queue,name):
        threading.Thread.__init__(self)
        self.queue = queue
        self.name = name
    """定义线程体"""
    def run(self):
        while True:
            page = self.queue.get()
            print (threading.current_thread().name,crawl_text(page))
            #需要对队列进行回收
            self.queue.task_done()


def crawl_text(page):
    date['pageNum'] = page
    response = requests.post(url,headers=headers,data=date).text
    return ("第{}已完成".format(page))
    # print (response)



if __name__ == '__main__':
    queue = queue.Queue()

    for page in range(1,101):
        queue.put(page)

    for i in range(100):
        work = MyThread(queue=queue,name='线程{0}'.format(i))
        work.daemon = True
        work.start()

    queue.join()
    print ('总用时：',time.time()-t1)
