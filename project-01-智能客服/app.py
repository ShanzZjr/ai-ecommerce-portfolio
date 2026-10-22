"""
电商智能客服 Demo（个人练手项目）
- 知识库检索 + 大模型问答 + 转人工规则
- 不填 key 进入「演示模式」，用规则命中返回示例答案，证明流程闭环
- 填 key 后调用免费大模型（DeepSeek / 通义千问 / OpenAI 任一）
"""
import re
from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import knowledge_base as kb

app = Flask(__name__)
app.secret_key = "demo-only-change-me"

PROVIDERS = {
    "deepseek": {"base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat"},
    "qwen":     {"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "model": "qwen-plus"},
    "openai":   {"base_url": "https://api.openai.com/v1", "model": "gpt-4o-mini"},
}

# 命中这些词，无论模型怎么答，都强制转人工（钱/订单/承诺/情绪/定制）
HANDOFF_TRIGGERS = ["退款", "订单", "物流单号", "催发", "投诉", "差评", "议价",
                    "优惠", "赠品", "改地址", "刻字", "定制", "赔偿", "赔付"]


def retrieve(query, top=3):
    """极简关键词检索：按词重叠打分，返回 top 条知识。"""
    words = set(re.findall(r"[\w\u4e00-\u9fff]+", query))
    scored = []
    for item in kb.KB:
        text = item["q"] + item["a"]
        score = sum(1 for w in words if w in text)
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: -x[0])
    return [i for _, i in scored[:top]]


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


@app.route("/chat", methods=["POST"])
def chat():
    query = request.json.get("query", "").strip()
    if not query:
        return jsonify({"answer": "请输入您的问题～", "handoff": False})
    hits = retrieve(query)
    client = get_client()

    # 演示模式：无 key 时用规则命中，证明整体流程
    if not client:
        if hits:
            return jsonify({
                "answer": hits[0]["a"], "source": hits[0]["q"],
                "handoff": False, "demo": True,
                "note": "演示模式（未接入大模型），命中知识库示例答案。"
            })
        return jsonify({
            "answer": "这个问题不在标准知识库内，已为您转接专属客服～",
            "handoff": True, "demo": True,
            "note": "演示模式：未命中知识库，按规则转人工。"
        })

    client, model = client
    ctx = "\n".join(f"问：{h['q']}\n答：{h['a']}" for h in hits)
    prompt = (
        "你是电商店铺售前客服，语气礼貌简洁。\n"
        "规则：\n"
        "1) 只能使用下面的【知识】回答，不要编造参数；\n"
        "2) 如果知识里没有、或用户问到退款/订单/投诉/议价/定制/赔付等，"
        "请只回复四个字【转人工】；\n"
        "3) 不确定时也要回复【转人工】。\n\n"
        f"【知识】\n{ctx}\n\n用户问题：{query}"
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        ans = resp.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"answer": f"调用大模型失败：{e}", "handoff": False, "error": True})

    handoff = ("转人工" in ans) or any(t in query for t in HANDOFF_TRIGGERS)
    # 若判定转人工，给出统一话术，避免模型瞎承诺
    if handoff and "转人工" not in ans:
        ans = "您的问题需要专属客服为您处理，已为您转接～"
    return jsonify({
        "answer": ans,
        "source": hits[0]["q"] if hits else "",
        "handoff": handoff,
        "demo": False,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
