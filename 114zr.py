import re
import queue
import threading
import requests

#多线程类
class Mythread(threading.Thread):
    
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
            page = self.queue.get()
            crawl_pageurl(page)
            self.queue.task_done()

def save(txt):
    with open('neir.txt','a') as f:
        f.write(txt + '\n')

def crawl_txt(endid):
    url2 = 'http://www.114zr.com/lost_display.php?id={}'.format(endid)
    res_detial = requests.get(url2).text
    re_list = ['<td height="38">师傅姓名:(.*?)&','; 性别:(.*?)<','<td height="38">工作地点:(.*?)&','; 工种类型:(.*?)<',"style='vertical-align:text-bottom' >:(.*?)<",'<td height="120" valign="top">([\s\S]*?)</td>','<td height="38">联系电话:([\s\S]*?)&','电子邮箱:([\s\S]*?)<br>']
    find_detial_list = []
    for i in re_list:
        find_detial = re.search(r'{}'.format(i),res_detial).group(1).strip().replace('\r', '').replace('\n','')
        find_detial_list.append(find_detial)
    find_detial_list.append(url2)
    save("|".join(find_detial_list))
    print("打印完成",endid)



def crawl_pageurl(page):
    url = 'http://www.114zr.com/zxsf.php?page={}'.format(page)
    res = requests.get(url).text
    find_endid = re.findall(r'<a href="lost_display.php\?id=(.*?)">',res)
    for endid in find_endid:
        crawl_txt(endid)


#单线程
# for page in range(1,65):
#     crawl_pageurl(page)
#     print('-----第{}页采集完毕------'.format(page))

#
