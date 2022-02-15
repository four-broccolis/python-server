from flask import Blueprint, Flask, jsonify
import pymysql
import copy

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
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
