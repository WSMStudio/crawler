import requests
import time
from threading import Thread
from queue import Queue
from parsel import Selector
import re
from guten_crawler2 import not_404

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
        self.range_start = 100000
        self.range_end = 500000
        self.thread_num = 10

    def produce_url(self):
        baseurl = "https://www.smashwords.com/books/view/{0}"
        for i in range(self.range_start, self.range_end):
            url = baseurl.format(i)
            self.qurl.put(url) # 生成URL存入队列，等待其他线程提取

    def get_info(self):
        while not self.qurl.empty(): # 保证url遍历结束后能退出线程
            url = self.qurl.get() # 从队列中获取URL
            bid = int(url.split("/")[-1])
            flag, res_text = not_404(url)
            if not flag:
                print(bid, "\033[33;1m404 or connection error\033[0m")
                continue
            selector = Selector(res_text)
            download_txt_links = [link for link in selector.css("#samples a").xpath("@href").getall()
                                  if link.endswith(".txt")] + \
                                 [link for link in selector.css("#download a").xpath("@href").getall()
                                  if link.endswith(".txt")]
            download_epub_links = [link for link in selector.css("#samples a").xpath("@href").getall()
                                   if link.endswith(".epub")] + \
                                  [link for link in selector.css("#download a").xpath("@href").getall()
                                   if link.endswith(".epub")]

            if not (download_epub_links or download_txt_links):
                print(f"{bid} don't have txt or epub links, next bid")
                continue
            title = selector.css("h1[itemprop='name']::text").extract_first()  # alias for get()
            authr = selector.css("meta[name='Author']").xpath('@content').extract_first()  # 在head里，方便爬虫使用的网页制作者写的
            descr = selector.css("meta[name='Description']").xpath('@content').extract_first()
            ptime = selector.css("li[itemprop='datePublished']").xpath('@content').extract_first()
            if download_txt_links:
                # print(download_txt_links)
                print(bid, "\033[32;1mhas txt\033[0m")
                text = str(bid) + "\thttps://www.smashwords.com" + download_txt_links[-1] + "\n"
                print(text)
                with open("./smash_data/content/not_crawled_url.txt", "a", encoding="utf-8") as f:
                    f.write(text)  # 如果有TXT,记录到./smash_data/not_crawled_url.txt
                # with open("./smash_data/content/not_crawled_url.txt", "a", encoding="utf-8") as f:
                #     f.write(text)  # 如果有TXT,记录到./smash_data/not_crawled_url.txt
            else:
                print(bid, "\033[34;1monly has epub\033[0m")
                epub = str(bid) + "\thttps://www.smashwords.com" + download_epub_links[-1] + "\n"
                print(epub)
                with open("./smash_data/smash_epub_1.txt", "a", encoding="utf-8") as f:
                    f.write(epub)  # 如果只有epub没有TXT,记录到./smash_data/smash_epub_1.txt
                # with open("./smash_data/smash_epub_1.txt", "a", encoding="utf-8") as f:
                #     f.write(epub)  # 如果只有epub没有TXT,记录到./smash_data/smash_epub_1.txt
            if not title:
                print(bid, "Not free, title")
            elif not authr:
                print(bid, "Not free, author")
            elif not ptime:
                print(bid, "Not free, ptime")
            else:
                authr = re.sub('[0-9\'!\"$%&\\\()*+\-/:<=>?@?★、…【】《》？“”！\[\]^_`{|}~]+', "", authr)
                ptime = ptime[:4]
                title = re.sub('[\n\t]', '', title)
                authr = re.sub('[\n\t]', '', authr)
                descr = re.sub('[\n\t]+', '', descr)
                print(f"{bid + 70000}\t{title}\t{authr}\t{ptime}\t{descr}\n")
                with open("./smash_data/smash_basic_info.txt", "a", encoding="utf-8") as f:
                    f.write(f"{bid + 70000}\t{title}\t{authr}\t{ptime}\t{descr}\n")
                # with open("./smash_data/smash_basic_info.txt", "a", encoding="utf-8") as f:
                #     f.write(f"{bid + 70000}\t{title}\t{authr}\t{ptime}\t{descr}\n")

            # self.titles.append(title)
            # self.bids.append(bid)

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

        # for i, datai in enumerate(self.titles):
        #     print(self.bids[i],datai)
        # with open('github_thread.json', 'w', encoding='utf-8') as f:
        #     f.write(s)

        # print('\nData crawling is finished.')

if __name__ == '__main__':
    Spider().run()

