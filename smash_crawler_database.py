import requests, time
from database_class import *
from parsel import Selector
import re

database = Database()
# database.count_text_epub()
url = "https://www.smashwords.com/books/view/{bid}"
for i in range(10268, 20000):
    res = requests.get(url.format(bid=i))
    if res.status_code == 404:
        print(i, "No Book")
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
        with open("./smash_data/smash_epub.txt", "a", encoding="utf-8") as f:
            f.write(epub)  # 如果只有epub没有TXT,记录下来
    if not content:
        print(i,"Not Free, content")
    elif not title:
        print(i,"Not free, title")
    elif not authr:
        print(i,"Not free, author")
    elif not ptime:
        print(i,"Not free, ptime")
    else:
        authr = re.sub('[0-9\'!\"$%&\\\()*+\-/:<=>?@?★、…【】《》？“”！\[\]^_`{|}~]+', "", authr)
        database.insert(i, title, authr, ptime[:4], descr, content)
    # if i % 500 == 0:
    #     database.count()
    time.sleep(0.3)

