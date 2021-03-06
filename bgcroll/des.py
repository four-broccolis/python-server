import feedparser
import re


def des(e):

    des = e.description

    targets = [
        "<.+?>",
        "&nbsp;",
        "&rarr;",
        "&lt;",
        "&gt;",
        "320x100",
        "SMALL",
        "LIST",
        "반응형",
    ]

    for target in targets:
        des = re.sub(target, "", des, 0).strip()

    des = re.sub("\n", " ", des, 0).strip()
    des = re.sub(" +", " ", des, 0).strip()
    des = re.sub("&#39;{0,1}", "", des, 0).strip()

    des = des[:150]

    return des


if __name__ == "__main__":
    url = "https://sookyeongyeom.github.io/feed.xml"

    d = feedparser.parse(url)

    e = d.entries[13]

    print(des(e))
