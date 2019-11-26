from io import BytesIO
import pycurl
import certifi
import pymysql
import json
import time
import warnings


def getData(url_token):
    tmp_queue = []
    tmp_follow_set = []
    for i in range(10000):
        time.sleep(2)
        url = "https://www.zhihu.com/api/v4/members/" + url_token + "/followees?include=data%5B*%5D.answer_count%2C" \
              "articles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F" \
              "(type%3Dbest_answerer)%5D.topics&offset=" + \
            str(i * 20) + "&limit=20"
        buffer = BytesIO()
        crl = pycurl.Curl()
        crl.setopt(crl.URL, url)
        crl.setopt(crl.WRITEDATA, buffer)
        crl.setopt(pycurl.CAINFO, certifi.where())
        try:
            crl.perform()
            crl.close()
            res = buffer.getvalue().decode('utf-8')
            data = json.loads(res)["data"]
        except Exception as err:
            return tmp_queue, tmp_follow_set
        if len(data) == 0:
            break
        for item in data:
            try:
                if item["user_type"] == "people":
                    tmp_url_token = item["url_token"]
                    tmp_queue.append(tmp_url_token)
                    tmp_follow_set.append((url_token, tmp_url_token))
            except:
                continue

    return tmp_queue, tmp_follow_set


if __name__ == "__main__":
    db = pymysql.connect(host='127.0.0.1', user='root',
                         passwd='1q2w3e4r', db='zhihu')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cur = db.cursor()
        print("Start Crawl")
        # 起点
        queue, follow_set = getData("leng-xie-49-83")
        cur.executemany("insert ignore into follow values(%s,%s)", follow_set)
        db.commit()
        time.sleep(2)
        print("init crawl")
        try:
            while len(queue) != 0:
                url_token = queue.pop(0)
                tmp_queue, tmp_follow_set = getData(url_token)
                cur.executemany(
                    "insert ignore into follow values(%s,%s)", tmp_follow_set)
                db.commit()
                time.sleep(2)
                queue.extend(tmp_queue)
        except:
            pass

        cur.close()
        db.close()
