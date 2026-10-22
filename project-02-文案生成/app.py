"""
商品文案生成 + 违禁词检测 Demo（个人练手项目）
- 输入品类/卖点/材质/颜色/尺寸 → 大模型生成 标题+五点+详情页大纲
- 生成后用本地违禁词表做极限词检测与高亮
- 不填 key 进入「演示模式」，返回模板化示例文案，证明流程闭环
"""
from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import banned_words as bw

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


def demo_copy(cat, points):
    return (
        f"【标题】{cat}通勤包 大容量百搭 单肩斜挎 女 2026新款\n"
        f"【五点描述】\n"
        f"1. 容量够大：可装手机/雨伞/13寸电脑，通勤出差都够用\n"
        f"2. 材质实在：头层牛皮+顺滑拉链，耐磨五金不掉色\n"
        f"3. 细节贴心：可调节肩带+多隔层分区，东西不乱塞\n"
        f"4. 百搭耐看：黑/奶茶/蓝三色，配裙子裤子都不违和\n"
        f"5. 售后省心：7天无理由，瑕疵包邮退换\n"
        f"【详情页结构】卖点图→尺寸容量图→材质细节→颜色实拍→背法展示→场景图→保养须知→售后说明"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/config", methods=["POST"])
def config():
    session["api_key"] = request.json.get("api_key", "")
    session["provider"] = request.json.get("provider", "deepseek")
    return jsonify({"ok": True, "has_key": bool(session.get("api_key"))})


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    cat = data.get("category", "").strip() or "包包"
    points = data.get("points", "").strip()
    material = data.get("material", "").strip()
    colors = data.get("colors", "").strip()
    size = data.get("size", "").strip()

    client = get_client()
    if not client:
        copy = demo_copy(cat, points)
        demo = True
    else:
        client, model = client
        prompt = (
            "你是电商文案专家。基于以下信息生成商品文案，严格只用给定信息，不要编造参数，"
            "不要使用极限词（最/第一/顶级等）。\n"
            f"品类：{cat}\n卖点：{points}\n材质：{material}\n颜色：{colors}\n尺寸：{size}\n\n"
            "输出格式：先【标题】（≤30字），再【五点描述】5条，再【详情页结构】8个板块名。"
        )
        try:
            resp = client.chat.completions.create(
                model=model, messages=[{"role": "user", "content": prompt}], temperature=0.6)
            copy = resp.choices[0].message.content.strip()
        except Exception as e:
            return jsonify({"copy": f"调用大模型失败：{e}", "hits": [], "demo": False, "error": True})
        demo = False

    hits = bw.check(copy)
    highlighted = bw.highlight(copy)
    return jsonify({"copy": copy, "highlighted": highlighted, "hits": hits, "demo": demo})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
