# -*- coding:utf-8 -*-\
import time
from ssl import _create_unverified_context
from json import loads
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter.messagebox
import urllib.request
import urllib.parse

class guterberg_crawler:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 设置为无头模式，即不显示浏览器
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"')  # 设置user=agent
        chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option("prefs",{"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                   "download.default_directory": "D:/chengxu2/WSM_crawler/data/text/"}
        chrome_options.add_experimental_option("prefs", profile)
        try:
            self.browser = webdriver.Chrome(executable_path='F:/chromedriver.exe',chrome_options=chrome_options)  # 设置chromedriver路径
            self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s
        except:
            print("chromedriver.exe出错，请检查是否与你的chrome浏览器版本相匹配\n缺失chromedriver.exe不会导致从排行榜搜索功能失效，但会导致从关键字搜索功能失效")

    def leave_max(self, filename = "./data/gutenberg_visited.txt"):
        file0 = open("./data/gutenberg_visited.txt", "r")
        visited = file0.readlines()
        if len(visited)>=1:
            max_num = int(visited[-1])
        else:
            max_num = -1
        file0.close()
        file1 = open("./data/gutenberg_visited.txt", "w")
        file1.write(str(max_num)+"\n")
        file1.close()
        return max_num

    def crawl_with_interval(self, start, end):
        url = "https://gutenberg.org/"
        max_visited = self.leave_max()
        file1 = open("./data/gutenberg_visited.txt", "a+")
        print("max_visited", max_visited)
        file2 = open("./data/gutenberg_attention.txt", "a+")
        file_object = open("./data/gutenberg"+str(start)+"-"+str(end-1)+".txt", 'a+', encoding='utf-8',buffering=-1)
        for i in range(start, end):
            if i <= max_visited:
                continue
            # 浏览网页
            current_url = url+"ebooks/"+str(i)
            # print("########################")
            # print("url: ", current_url)
            self.browser.get(current_url)
            # 判断是否页面不存在，不存在也要保存该网址代表已经去过，
            if len(self.browser.find_elements_by_xpath('//*[@id="page_content"]/h1')) >= 1:
                print("This page {0} doesn't exist, ignored,".format(current_url))
                file1.write(str(i)+'\t')
                continue
            # 存在的话就爬数据，爬url，
            bibliography = crawler.browser.find_element_by_id('bibrec')
            author_element = bibliography.find_elements_by_xpath('//*[contains(text(),"Author")]/following-sibling::td')
            author_num = len(author_element)
            if author_num >= 1:
                authors = []
                for j in author_element:
                    authors.append(j.text) # 需要去除生卒年份
                author = "# ".join(authors)
                if author_num > 1:
                    file2.write(str(i)+" multi-author:{0}\n".format(author_num))
            else:
                author = "Unknown"
            # print(author)
            title_element = bibliography.find_elements_by_xpath('//*[contains(text(),"Title")]/following-sibling::td')
            if len(title_element) >= 1:
                title = title_element[0].text.replace("\n"," ") #需要去除\n符号
            else:
                title = "Unknown"
            # print(title)
            publish_element = bibliography.find_elements_by_xpath('//*[contains(text(),"Release Date")]/following-sibling::td')
            if len(publish_element) >= 1:
                publish_year = publish_element[0].text[:4]
            else:
                publish_year = "Unknown"
            # print(publish_year)
            description = 'No description'
            # print(description)
            content_url = 0
            download_options = ['Plain Text UTF-8', 'PDF', 'EPUB (no images)', 'EPUB (with images)', 'Kindle (no images)','Kindle (with images)','Plain Text US-ASCII','HTML','RDF','Plain Text']
            for opt in download_options:
                content_element = crawler.browser.find_elements_by_link_text(opt)
                if len(content_element) >= 1:
                    content_url = content_element[0].get_attribute('href')
                    break
            if content_url == 0:
                print("\033[31;1mNo content for this book, ignored\033[0m")
                file2.write(str(i)+" No content\n")
                continue
            # print("content_url: ", content_url)  # 已经带了http
            # 保存数据
            print("{0:<35}\t{1:<}\t{2:<}\t{3:<5}\t{4:<15}\t{5:<}".format(current_url,author,title,publish_year,description,content_url))
            file_object.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(current_url,author,title,publish_year,description,content_url))
            file1.write(str(i)+'\n')
            # 下载 text URL？

        # 关闭浏览器
        file_object.close()
        file1.close()
        file2.close()
        self.browser.quit()

crawler = guterberg_crawler()

i = 1 #一次5000，到65000本书，最后还有不到1000本
crawler.crawl_with_interval(i*5000,(i+1)*5000)
# crawler.crawl_with_interval(65000,66000)