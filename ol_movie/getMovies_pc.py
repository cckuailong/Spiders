from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import json
import time
import requests
from requests.adapters import HTTPAdapter
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Movie:
    def __init__(self, id):
        self.id = id
        self.title = ''
        self.actors = ''
        self.region = ''
        self.desc = ''
        self.urls = []
        
    def getCont(self):                
        s = requests.Session()
        s.keep_alive = False
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        headers = {
            'X-Forwarded-For': '%s.%s.%s.%s'%(random.randint(1,255),random.randint(1,255),random.randint(1,255),random.randint(1,255)),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
        }
        url = 'http://my.derjung.cn/index.php/vod/play/id/{}'.format(self.id)
        try:
            resp = s.get(url, headers=headers, verify=False, timeout=5)
            if resp.status_code == 200:
                with open("movie.html", "w", encoding="utf8") as f:
                    f.write(resp.text)
        except Exception as err:
            print(err)

    def getUrl(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")

        browser = webdriver.Chrome(options=options)
        browser.get(url)
        res = browser.find_element_by_class_name('embed-responsive-item').get_attribute("src")
        browser.close()

        return res


    def parse(self):    
        with open("movie.html", "r", encoding="utf8") as f:
            cont = f.read()
        res = {}
        if not cont:
            return json.dumps(res)
        sp = BeautifulSoup(cont, "lxml")

        try:
            inputs = sp.find_all("ul", "stui-content__playlist clearfix")[0].find_all("a")
            for item in inputs:
                try:
                    tmp_url = "http://my.derjung.cn/"+item["href"].strip()
                    self.urls.append({item.text.strip(): self.getUrl(tmp_url)})
                except:
                    pass
        except:
            pass
        if len(self.urls) == 0:
            return json.dumps(res)
        try:
            self.title = sp.find_all("h4", "title")[0].text
        except:
            pass
        try:
            aes = sp.find_all("p", "data margin-0")[0].find_all("a")
            self.region = aes[1].text.strip()
        except:
            pass
        try:
            divs = sp.find_all("div", "stui-content__desc col-pd clearfix")
            self.desc = divs[0].text.strip()
        except:
            pass

        res = {"title":self.title, "actors":self.actors, "region":self.region, "desc":self.desc, "urls":self.urls}

        return json.dumps(res)

    

if __name__ == "__main__":
    for i in range(1571, 60000):
        print(i)
        movie = Movie(i)
        movie.getCont()
        try:
            res = movie.parse()
        except:
            continue
        with open("movies.csv", "a", encoding="utf8") as f:
            if len(res)>10:
                f.write("%s\t%s\n" % (i, res))
        time.sleep(random.randint(1,5))
