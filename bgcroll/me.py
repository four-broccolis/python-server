import feedparser


url = "https://sookyeongyeom.github.io/feed.xml"

d = feedparser.parse(url)

print(d.entries[0].content[1]["value"])
