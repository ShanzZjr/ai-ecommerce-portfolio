# -*- coding: utf-8 -*-
"""项目四：经营数据日报生成器（演示模式无需 API key）

POST /report  body 可选 {"rows": [...]}，缺省读 sample_data.csv
"""
from flask import Flask, request, jsonify, render_template
import report_analyzer as ra

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sample")
def sample():
    rows = ra.load_sample()
    return jsonify({"count": len(rows), "rows": rows})


@app.route("/report", methods=["POST"])
def report():
    body = request.get_json(silent=True) or {}
    rows = body.get("rows") or []
    if not rows:
        rows = ra.load_sample()  # 演示模式：用示例数据跑通全流程
    try:
        result = ra.analyze(rows)
    except Exception as e:
        return jsonify({"error": "解析失败：%s（请检查列名：日期/访客数/浏览量/支付买家数/支付金额/退款金额/加购人数/收藏人数）" % e}), 400
    result["mode"] = "演示模式（纯规则生成，可解释可审计；接入大模型可口语化润色）"
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=True)
