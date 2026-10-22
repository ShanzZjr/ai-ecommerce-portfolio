# -*- coding: utf-8 -*-
"""项目六：短视频 / 直播脚本批量生成（演示模式无需 API key）

POST /generate  {"product": "托特包", "points": "大容量,百搭", "price": "129", "audience": "通勤女生"}
"""
from flask import Flask, request, jsonify, render_template
import script_templates as st

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    body = request.get_json(silent=True) or {}
    result = st.demo_generate(
        product=body.get("product"),
        points=body.get("points"),
        price=body.get("price"),
        audience=body.get("audience"),
    )
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
