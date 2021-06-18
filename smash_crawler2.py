import requests, time
from parsel import Selector
import re
from guten_crawler2 import not_404


if __name__ == '__main__':
    url = "https://www.smashwords.com/books/view/{bid}"
    for i in range(18983, 60000):
        flag, res_text = not_404(url.format(bid=i))
        if not flag:
            print(i, "404 or connection error")
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

        #爬下来如果至少有text和epub中的一个，就存basic信息，并且在content的not_crawled_url.txt里留下txt的bid及url 或者 在
        #smash_epub_1.txt里留下epub的bid及url。 不用爬content，只需要留下content的url

        if not (download_epub_links or download_txt_links):
            print(f"{i} don't have txt or epub links, next bid")
            continue
        title = selector.css("h1[itemprop='name']::text").extract_first()  # alias for get()
        authr = selector.css("meta[name='Author']").xpath('@content').extract_first()  # 在head里，方便爬虫使用的网页制作者写的
        descr = selector.css("meta[name='Description']").xpath('@content').extract_first()
        ptime = selector.css("li[itemprop='datePublished']").xpath('@content').extract_first()
        if download_txt_links:
            # print(download_txt_links)
            print(str(i)+"\033[32;1mhas txt\033[0m")
            text = str(i) + "\thttps://www.smashwords.com" + download_txt_links[-1] + "\n"
            with open("./smash_data/content/not_crawled_url.txt", "a", encoding="utf-8") as f:
                f.write(text)  # 如果有TXT,记录到./smash_data/not_crawled_url.txt
        else:
            print(str(i) + "\033[34;1monly has epub\033[0m")
            epub = str(i)+"\thttps://www.smashwords.com"+download_epub_links[-1]+"\n"
            with open("./smash_data/smash_epub_1.txt", "a", encoding="utf-8") as f:
                f.write(epub)  # 如果只有epub没有TXT,记录到./smash_data/smash_epub_1.txt
        if not title:
            print(i,"Not free, title")
        elif not authr:
            print(i,"Not free, author")
        elif not ptime:
            print(i,"Not free, ptime")
        else:
            authr = re.sub('[0-9\'!\"$%&\\\()*+\-/:<=>?@?★、…【】《》？“”！\[\]^_`{|}~]+', "", authr)
            ptime = ptime[:4]
            title = re.sub('[\n\t]', '', title)
            authr = re.sub('[\n\t]', '', authr)
            descr = re.sub('[\n\t]+', '', descr)
            with open("./smash_data/smash_basic_info.txt", "a", encoding="utf-8") as f:
                f.write(f"{i+70000}\t{title}\t{authr}\t{ptime}\t{descr}\n")
        # time.sleep(0.3)

