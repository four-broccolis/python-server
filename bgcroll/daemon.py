import json
import pymysql
import feedparser
from datetime import datetime

# DB 연결
conn = pymysql.connect(user='sky', passwd='7173',
                       host='127.0.0.1', db='rss', charset='utf8')
cursor = conn.cursor()

# Info 가져오기
f = open("info.json", "r", encoding='UTF-8')
info = json.load(f)
platforms = ['tistory', 'velog', 'naver', 'git']

# Topic 가져오기
f = open("topic.json", "r", encoding='UTF-8')
topic = json.load(f)

# 스크립트 시작 시 세팅
recent = {}
for platform in platforms:
    print("[System] Setting "+platform+"...")
    platform = info[platform]
    keys = list(platform.keys())
    for key in keys:
        name = key
        url = platform[name]
        query = "SELECT * FROM post where name=%s order by published desc"
        cursor.execute(query, name)
        result = cursor.fetchone()
        if result:
            recent[name] = result[4]

print("")

# 실시간 비교
while True:
    for platform in platforms:
        now = platform.capitalize()
        print("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
              "] Monitoring " + platform + "...")
        platform = info[platform]
        keys = list(platform.keys())
        for key in keys:
            name = key
            mytopic = topic[name[:3]]
            url = platform[name]
            d = feedparser.parse(url)
            try:
                e = d.entries[0]
                if now == "Git":
                    date = e.published.split("+")
                    date = date[0]
                    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
                else:
                    date = e.published.split(" ")
                    date = date[1]+" "+date[2]+" "+date[3]+" "+date[4]
                    date = datetime.strptime(date, "%d %b %Y %H:%M:%S")

                if recent[name] == date:
                    continue
                elif recent[name] < date:
                    recentdate = date
                    data = []
                    for e in d.entries:
                        title = e.title
                        link = e.link
                        # 예정 : Git인 경우 date 파싱 따로
                        date = e.published.split(" ")
                        date = date[1]+" "+date[2]+" "+date[3]+" "+date[4]
                        date = datetime.strptime(date, "%d %b %Y %H:%M:%S")
                        if recent[name] < date <= recentdate:
                            thisdata = (name, title, link, date, mytopic, now)
                            data.append(thisdata)
                        else:
                            break
                    print("💡 "+name+"님의 최신 글이 " +
                          str(len(data))+"개 있습니다! DB에 반영합니다.")
                    query = "INSERT INTO post (id, name, title, link, published, topic, platform) VALUE (0, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(query, data)
                    conn.commit()
                    recent[name] = recentdate
                else:
                    pass
            except:
                # print(name+"님은 활동 기록이 없습니다.")
                continue
