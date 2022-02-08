import json
import pymysql
import feedparser
from datetime import datetime

# Tistory, Velog, Naver
def getdate(e):
    date = e.published.split(" ")
    date = date[1] + " " + date[2] + " " + date[3] + " " + date[4]
    date = datetime.strptime(date, "%d %b %Y %H:%M:%S")
    return date


# Git
def getdate_git(e):
    date = e.published.split("+")
    date = date[0]
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    return date


# DB 연결
conn = pymysql.connect(
    user="sky", passwd="7173", host="127.0.0.1", db="rss", charset="utf8"
)
cursor = conn.cursor()

# Info 가져오기
f = open("info.json", "r", encoding="UTF-8")
info = json.load(f)
platforms = ["tistory", "velog", "naver", "git"]

# Topic 가져오기
f = open("topic.json", "r", encoding="UTF-8")
topic = json.load(f)

# 스크립트 시작 시 세팅
recent = {}
for platform in platforms:
    print("[System] Setting " + platform + "...")
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
        print(
            "["
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + "] Monitoring "
            + platform
            + "..."
        )
        platform = info[platform]
        keys = list(platform.keys())
        for key in keys:
            name = key
            mytopic = topic[name[:3]]
            url = platform[name]
            d = feedparser.parse(url)
            try:
                e = d.entries[0]  # 현재 블로그에 게시된 게시글 중 가장 최신 글
                if now == "Git":
                    date = getdate_git(e)
                else:
                    date = getdate(e)

                if name in recent.keys():  # 일반적인 경우
                    if recent[name] == date:  # DB 최신글 == 실제 최신글
                        continue
                    elif recent[name] < date:  # DB 최신글 < 실제 최신글
                        recentdate = date
                        data = []
                        for e in d.entries:
                            title = e.title
                            link = e.link
                            if now == "Git":
                                date = getdate_git(e)
                            else:
                                date = getdate(e)
                            if recent[name] < date <= recentdate:
                                thisdata = (name, title, link, date, mytopic, now)
                                data.append(thisdata)
                            else:
                                break
                        print(
                            "💡 "
                            + name
                            + "님의 최신 글이 "
                            + str(len(data))
                            + "개 있습니다! DB에 반영합니다."
                        )
                        query = "INSERT INTO post (id, name, title, link, published, topic, platform) VALUE (0, %s, %s, %s, %s, %s, %s)"
                        cursor.executemany(query, data)
                        conn.commit()
                        recent[name] = recentdate
                    else:
                        pass  # 기존 게시글이 삭제된 경우 (RSS 피드에는 삭제 내역이 반영되지 않으므로 발생하지 않음)

                else:  # 초기세팅 시 DB에 첫 글이 없었을 경우
                    recentdate = date
                    for e in d.entries:
                        title = e.title
                        link = e.link
                        if now == "Git":
                            date = getdate_git(e)
                        else:
                            date = getdate(e)
                        thisdata = (name, title, link, date, mytopic, now)
                        data.append(thisdata)
                    print(
                        "🎉 " + name + "님의 첫 글이 " + str(len(data)) + "개 있습니다! DB에 반영합니다."
                    )
                    query = "INSERT INTO post (id, name, title, link, published, topic, platform) VALUE (0, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(query, data)
                    conn.commit()
                    recent[name] = recentdate  # recent에 새로운 키-값 생성

            except Exception as e:  # 대부분 아무 글도 없는 경우 에러 발생
                try:
                    anypost = d.entries[0]  # 게시글 존재 여부 확인
                    print("❗ 에러가 발생했습니다. [" + e + "]")
                except:
                    print("❗ " + name + "님은 아무 포스팅도 게시하지 않았습니다.")
                continue
