from db import *
import re

def save_text_all(Bid):
    values = database.cursor.execute('''SELECT BID,TITLE,AUTHR,PTIME,DESCR,CONTENT FROM BOOKS''')
    text_bid_list, epub_bid_list, text_count, epub_count = [], [], 0, 0
    for bid, title, authr, ptime, descr, cont in values:
        if bid <= Bid:
            continue
        if len(cont) > 4:
            text_count += 1
            text_bid_list.append(bid)

            bid += 70000
            title = re.sub('[\n\t]', '', title)
            authr = re.sub('[\n\t]', '', authr)
            descr = re.sub('[\n\t]+', '', descr)
            with open("./smash_data/smash_basic_info.txt", "a", encoding="utf-8") as f:
                f.write(f"{bid}\t{title}\t{authr}\t{ptime}\t{descr}\n")
            if cont[0:9] == "<!DOCTYPE":
                with open(f"./smash_data/content/not_crawled.txt", "a", encoding="utf-8") as f1:
                    f1.write(f"{bid-70000}\t")
                pass
            else:
                # with open(f"./smash_data/content/pa{bid}.txt", "w", encoding="utf-8") as f1:
                #     f1.write(cont)
                pass
        else:
            epub_count+=1
            epub_bid_list.append(bid)
    print(f"Count of books have Text is {text_count}, epub is {epub_count}")
    print(text_bid_list)
    with open("./smash_data/smash_text_bid.txt", "w", encoding="utf-8") as f2:
        for i in text_bid_list:
            f2.write(f"{i}\t")
database = Database()
save_text_all(0)

