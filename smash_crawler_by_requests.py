import requests, time
from db import *
from parsel import Selector
import re

database = Database()
url = "https://www.smashwords.com/books/view/{bid}"
f = open("./smash_data/smash_epub.txt", "a", encoding="utf-8")
for i in range(3, 20000):
    res = requests.get(url.format(bid=i))
    if res.status_code == 404:
        print("No Book", i)
        continue
    selector = Selector(res.text)

    title = selector.css("h1[itemprop='name']::text").extract_first() # alias for get()
    authr = selector.css("meta[name='Author']").xpath('@content').extract_first() # 在head里，方便爬虫使用的网页制作者写的
    descr = selector.css("meta[name='Description']").xpath('@content').extract_first()
    ptime = selector.css("li[itemprop='datePublished']").xpath('@content').extract_first()
    download_txt_links = [link for link in selector.css("#samples a").xpath("@href").getall()
                      if link.endswith(".txt")] + \
        [link for link in selector.css("#download a").xpath("@href").getall()
                      if link.endswith(".txt")]
    download_epub_links = [link for link in selector.css("#samples a").xpath("@href").getall()
                      if link.endswith(".epub")] + \
        [link for link in selector.css("#download a").xpath("@href").getall()
                      if link.endswith(".epub")]
    if not (download_epub_links or download_txt_links):
        content = ""
        epub = ""
    elif download_txt_links:
        # print(download_txt_links)
        content = requests.get("https://www.smashwords.com" + download_txt_links[-1]).text
        print(str(i)+"\033[32;1mhas txt\033[0m")
        epub = ""
    else:
        content = "epub"
        print(str(i) + "\033[31;1monly has epub\033[0m")
        epub = str(i)+"\t"+download_epub_links[-1]+"\n"

    if epub:
        f.write(epub)  # 如果只有epub没有TXT,记录下来
    if not content:
        print("Not Free, content", i)
    elif not title:
        print("Not free, title", i)
    elif not authr:
        print("Not free, author", i)
    elif not ptime:
        print("Not free, ptime", i)
    else:
        authr = re.sub('[0-9\'!\"$%&\\\()*+\-/:<=>?@?★、…【】《》？“”！\[\]^_`{|}~]+', "", authr)
        database.insert(i, title, authr, ptime[:4], descr, content)
        database.printb(title)
    # time.sleep(0.3)

f.close()