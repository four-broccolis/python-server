from flask import Blueprint, Flask, jsonify
import pymysql
import copy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def send_post():
    conn = pymysql.connect(
        user="sky", passwd="7173", host="localhost", db="rss", charset="utf8"
    )
    cursor = conn.cursor()
    query = "SELECT * FROM post_des order by published desc limit 30"
    cursor.execute(query)
    result = cursor.fetchall()
    subject = [
        "name",
        "title",
        "description",
        "link",
        "published",
        "topic",
        "platform",
    ]
    posts = []
    post = {}
    for res in result:
        for i, row in enumerate(res):
            if i == 0:
                continue
            post[subject[i - 1]] = res[i]
        posts.append(copy.deepcopy(post))
    return jsonify(posts)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
