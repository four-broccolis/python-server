import json
import pymysql
import feedparser
from datetime import datetime

f = open("info.json", "r", encoding='UTF-8')
status = json.load(f)
tistory = status['tistory']
velog = status['velog']
naver = status['naver']
git = status['git']

f = open("topic.json", "r", encoding='UTF-8')
topic = json.load(f)

conn = pymysql.connect(user='sky', passwd='7173',
                       host='127.0.0.1', db='rss', charset='utf8')
cursor = conn.cursor()


def croll_type1(platform, topic, platname):
    for i in range(0, len(platform)):
        name = list(platform.keys())[i]
        mytopic = topic[name[:3]]
        url = platform[name]
        d = feedparser.parse(url)
        print(name, d.feed['title'])
        for e in d.entries:
            title = e.title
            link = e.link
            date = e.published.split(" ")
            date = date[1]+" "+date[2]+" "+date[3]+" "+date[4]
            date = datetime.strptime(date, "%d %b %Y %H:%M:%S")
            data = (name, title, link, date, mytopic, platname)
            query = "INSERT INTO post (id, name, title, link, published, topic, platform) VALUE (0, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, data)
            conn.commit()


def croll_type2(platform, topic, platname):
    for i in range(0, len(platform)):
        name = list(platform.keys())[i]
        mytopic = topic[name[:3]]
        url = platform[name]
        d = feedparser.parse(url)
        print(name, d.feed['title'])
        for e in d.entries:
            title = e.title
            link = e.link
            date = e.published.split("+")
            date = date[0]
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
            data = (name, title, link, date, mytopic, platname)
            query = "INSERT INTO post (id, name, title, link, published, topic, platform) VALUE (0, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, data)
            conn.commit()


if __name__ == '__main__':
    croll_type1(tistory, topic, "Tistory")
    croll_type1(velog, topic, "Velog")
    croll_type1(naver, topic, "Naver")
    croll_type2(git, topic, "Git")
