import feedparser
from des import des
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


d = feedparser.parse("https://keykat7.blogspot.com/feeds/posts/default?alt=rss")

for e in d.entries:
    title = e.title
    link = e.link
    description = des(e)
    date = getdate(e)
    print(date)
