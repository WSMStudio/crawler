import requests
import time
from threading import Thread
from queue import Queue
from parsel import Selector

def calculate_run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print('running ', end-start, 's')
    return wrapper

class Spider():

    def __init__(self):
        self.qurl = Queue()
        self.titles = list()
        self.bids = list()
        self.range_start = 1
        self.range_end = 100
        self.thread_num = 10

    def produce_url(self):
        baseurl = "https://www.smashwords.com/books/view/{0}"
        for i in range(self.range_start, self.range_end):
            url = baseurl.format(i)
            self.qurl.put(url) # 生成URL存入队列，等待其他线程提取

    def get_info(self):
        while not self.qurl.empty(): # 保证url遍历结束后能退出线程
            url = self.qurl.get() # 从队列中获取URL
            bid = url.split("/")[-1]
            # print('crawling ', url.split("/")[-1])
            response = requests.get(url)
            if response.status_code == 404:
                print(bid, "No Book")
                continue
            selector = Selector(response.text)
            title = selector.css("h1[itemprop='name']::text").extract_first()
            if not title:
                print(bid, "No title")
                continue
            self.titles.append(title)
            self.bids.append(bid)

    @calculate_run_time
    def run(self):
        self.produce_url()

        ths = []
        for _ in range(self.thread_num):
            th = Thread(target=self.get_info)
            th.start()
            ths.append(th)
        for th in ths:
            th.join()

        for i, datai in enumerate(self.titles):
            print(self.bids[i],datai)
        # with open('github_thread.json', 'w', encoding='utf-8') as f:
        #     f.write(s)

        print('Data crawling is finished.')

if __name__ == '__main__':
    Spider().run()

