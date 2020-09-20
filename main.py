#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 15:53:47 2020

@author: user
"""

import requests
from urllib.request import urlopen
from lxml import etree
from bs4 import BeautifulSoup 
import shutil
import json
import time


base_url = "https://ask.fm"
user = f"/{input('Enter the username: ')}"
# user = "/Abufhr?iterator=69200&older=1488557300"

response = requests.get(base_url + user)
soup = BeautifulSoup(response.content, "html.parser")

items = []

item_page_tag = soup.select_one(".item-page:nth-last-child(2)")
page = 0

while item_page_tag:
    page += 1
    
    for article_tag in item_page_tag.select("article.item.streamItem.streamItem-answer"):
        item = {}
        item["question"] = article_tag.select_one(".streamItem_header>h2").text
        item["time"] = article_tag.select_one(".streamItem_properties time")["datetime"]
        item["link"] = article_tag.select_one(".streamItem_properties a")["href"]
        
        answer = article_tag.select(".streamItem_content > span, .streamItem_content > a")
        if answer:
            item["text_answer"] = "\n".join(map(lambda tag: tag.text, answer))
        
        image_tag = article_tag.select_one(".streamItem_visual > div > a > img")
        if image_tag:
            # r = requests.get(image_tag["src"], stream = True)
            # item["img_answer"] = r.raw.read(decode_content = True)
            item["img_answer_url"] = image_tag["src"]
            
        items.append(item)
    next_page_url =  soup.select_one(".item-page-next")["href"]
    
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    response = requests.get(base_url + next_page_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    item_page_tag = soup.select_one(".item-page:nth-last-child(2)")
    
    if not item_page_tag:
        print("[-] No more pages!!")
        break
    
    print(f"to parse: page #{page} ({next_page_url})")
    
    if page % 100 == 0:
        with open(f"{user[1:]}_{page}.json", "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False)
        
        items.clear()
        time.sleep(60)
        

    