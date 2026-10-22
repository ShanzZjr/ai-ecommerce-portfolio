# 极限词 / 违禁词表（电商合规，重点针对包包等服饰百货）
# 来源：广告法常见违禁词 + 平台规则高频词。真实使用请结合最新平台规则更新。
# 每条: word=词, reason=原因/风险

BANNED = [
    {"word": "最", "reason": "绝对化用语，广告法明令禁止（如最好/最大）"},
    {"word": "第一", "reason": "绝对化排名，需权威证明，普通店铺禁用"},
    {"word": "顶级", "reason": "绝对化用语"},
    {"word": "极致", "reason": "绝对化用语"},
    {"word": "极佳", "reason": "绝对化用语"},
    {"word": "完美", "reason": "绝对化用语"},
    {"word": "绝对", "reason": "绝对化用语"},
    {"word": "国家级", "reason": "绝对化/误导，广告法禁止"},
    {"word": "全网最低", "reason": "价格误导，无法证明"},
    {"word": "史上最", "reason": "绝对化用语"},
    {"word": "销量第一", "reason": "排名绝对化，需证明"},
    {"word": "唯一", "reason": "绝对化用语"},
    {"word": "王牌", "reason": "夸大宣传"},
    {"word": "极品", "reason": "绝对化用语"},
    {"word": "100%真皮", "reason": "笼统真皮表述易误导，须写具体皮料部位"},
    {"word": "原单", "reason": "易涉侵权/虚假来源"},
    {"word": "尾货", "reason": "易涉虚假来源"},
    {"word": "专柜同款", "reason": "易涉侵权"},
    {"word": "正品代工", "reason": "易涉虚假宣传"},
    {"word": "永久", "reason": "绝对化用语"},
    {"word": "万能", "reason": "绝对化用语"},
]


def check(text):
    """返回命中列表：[{word, reason, count}]，按出现次数降序。"""
    hits = []
    for item in BANNED:
        c = text.count(item["word"])
        if c > 0:
            hits.append({"word": item["word"], "reason": item["reason"], "count": c})
    hits.sort(key=lambda x: -x["count"])
    return hits


def highlight(text):
    """把命中词用 << >> 包起来，方便前端高亮（前端再转成红色 span）。"""
    result = text
    for item in BANNED:
        if item["word"] in result:
            result = result.replace(item["word"], f"<<{item['word']}>>")
    return result
