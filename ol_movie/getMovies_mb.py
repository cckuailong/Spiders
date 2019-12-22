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

base_url = "http://my.nxycyyh.com/"

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
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
        }
        url = '{}index.php/vod/play/id/{}'.format(base_url, self.id)
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
        options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')

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
            inputs = sp.find("div", "video_list fn-clear").find_all("a")
            for item in inputs:
                try:
                    tmp_url = base_url+item["href"].strip()
                    self.urls.append({item.text.strip(): self.getUrl(tmp_url)})
                except Exception as err:
                    print(err)
        except Exception as err:
            print(err)
        if len(self.urls) == 0:
            return json.dumps(res)
        try:
            self.title = str(sp.title.text).split(" ")[0].strip()
        except Exception as err:
            print(err)

        try:
            dds = sp.find("div", "info fn-clear")
            infos = dds.find_all("dd")
            self.actors = infos[0].text
            self.region = infos[2].text
        except Exception as err:
            print(err)
        try:
            self.desc = sp.find("div", "tjuqing").find("p").text
        except Exception as err:
            print(err)

        res = {"title":self.title, "actors":self.actors, "region":self.region, "desc":self.desc, "urls":self.urls}

        return json.dumps(res)

    

if __name__ == "__main__":
    for i in range(2670, 60000):
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
