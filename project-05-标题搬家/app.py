# -*- coding: utf-8 -*-
"""项目五：多平台标题搬家 + SEO 优化（演示模式无需 API key）

POST /adapt  {"title": "原标题", "category": "托特包", "points": "大容量,百搭"}
"""
from flask import Flask, request, jsonify, render_template
import platform_rules as pr

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/adapt", methods=["POST"])
def adapt():
    body = request.get_json(silent=True) or {}
    title = (body.get("title") or "").strip()
    if not title:
        return jsonify({"error": "请提供原标题 title"}), 400
    category = (body.get("category") or "").strip() or "托特包"
    points = body.get("points") or ""
    results = pr.demo_adapt(title, category, points)
    banned_total = sum(len(r["banned"]) for r in results)
    return jsonify({
        "results": results,
        "banned_total": banned_total,
        "mode": "演示模式（规则模板生成；接入大模型可升级为语义改写）",
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5004, debug=True)
