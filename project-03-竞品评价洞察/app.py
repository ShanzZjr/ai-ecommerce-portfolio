"""
竞品/店铺评价洞察 Demo（个人练手项目）
- 导入示例评价数据 → 情感分类 + 差评归因 + 改进清单
- 演示模式（无 key）：规则分析，证明流程闭环
- 填 key 后：大模型在规则结果上生成一段给运营的自然语言总结
"""
import os
from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import analyze as az

app = Flask(__name__)
app.secret_key = "demo-only-change-me"

PROVIDERS = {
    "deepseek": {"base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat"},
    "qwen":     {"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "model": "qwen-plus"},
    "openai":   {"base_url": "https://api.openai.com/v1", "model": "gpt-4o-mini"},
}


def get_client():
    key = session.get("api_key", "")
    prov = session.get("provider", "deepseek")
    if not key:
        return None
    cfg = PROVIDERS.get(prov, PROVIDERS["deepseek"])
    return OpenAI(api_key=key, base_url=cfg["base_url"]), cfg["model"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/config", methods=["POST"])
def config():
    session["api_key"] = request.json.get("api_key", "")
    session["provider"] = request.json.get("provider", "deepseek")
    return jsonify({"ok": True, "has_key": bool(session.get("api_key"))})


@app.route("/sample")
def sample():
    return jsonify({"reviews": az.load_sample()})


@app.route("/analyze", methods=["POST"])
def analyze():
    reviews = request.json.get("reviews", [])
    if not reviews:
        reviews = az.load_sample()
    result = az.analyze(reviews)

    client = get_client()
    if client:
        client, model = client
        prompt = (
            "你是电商运营分析师。基于评价分析数据，给运营负责人写一段中文总结（≤200字），"
            "点出最该优先解决的2个问题及原因。\n"
            f"情感分布：{result['sentiment']}\n差评归因：{result['attribute']}"
        )
        try:
            resp = client.chat.completions.create(
                model=model, messages=[{"role": "user", "content": prompt}], temperature=0.5)
            result["summary"] = resp.choices[0].message.content.strip()
        except Exception as e:
            result["summary"] = f"大模型总结失败：{e}"
    else:
        result["summary"] = "（演示模式）未接入大模型，下面是规则分析结果，可据此人工写总结。"
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
