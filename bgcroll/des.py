import feedparser
import re


def des(name, e):

    if name == "염수경":
        des = e.content[1]["value"]
    else:
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

    des = des[:100]

    return des


if __name__ == "__main__":
    url = "https://v2.velog.io/rss/@broccolism"

    d = feedparser.parse(url)

    e = d.entries[13]

    print(des(e))
