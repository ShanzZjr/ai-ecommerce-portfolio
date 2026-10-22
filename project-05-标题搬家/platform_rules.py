# -*- coding: utf-8 -*-
"""多平台标题适配：平台规则 + 违禁词检测 + 演示模式生成器。

设计原则（面试可讲）：
- 平台差异沉淀为配置表（字数上限 + 风格模板），一换配置即可扩展新平台；
- 生成后强制过本地违禁词表 —— 生成 + 合规校验闭环，与项目二同思路。
"""

# 极限词 / 违禁词表（示例，可按最新广告法与平台规则扩充）
BANNED = ["最", "第一", "顶级", "绝对", "全网最低", "100%", "国家级",
          "销量第一", "独家", "首选", "王牌", "万能", "假一赔十"]

# 平台规则配置表
PLATFORMS = [
    {"name": "淘宝",   "max": 30, "style": "关键词规整堆叠：核心词+属性词+长尾词，利于搜索"},
    {"name": "拼多多", "max": 60, "style": "高密度堆词+营销词（工厂直发/特价/包邮）"},
    {"name": "抖音",   "max": 55, "style": "口语化+场景痛点+情绪钩子，适配短视频口播"},
    {"name": "小红书", "max": 20, "style": "种草分享风，弱营销、强体验词"},
]


def check_banned(text):
    hits = []
    for w in BANNED:
        c = text.count(w)
        if c:
            hits.append({"word": w, "count": c})
    return hits


def _points(points):
    ps = [p.strip() for p in (points or "").replace("，", ",").replace("、", ",").split(",") if p.strip()]
    return ps or ["大容量", "百搭"]


def _cut(s, n):
    return s[:n]


def demo_adapt(title, category, points):
    """演示模式：规则模板生成四平台标题（接入大模型可升级为语义改写）。"""
    core = (title or "").strip() or (category or "托特包")
    cat = (category or "托特包").strip()
    cat_in_core = bool(cat) and cat in core  # 原标题已含类目词时避免重复堆词
    pt = _points(points)
    pt2 = " ".join(pt[:2])

    drafts = {
        "淘宝":   ("%s %s 官方正品 包邮" % (core, pt2) if cat_in_core
                   else "%s %s %s 官方正品 包邮" % (cat, pt2, core)),
        "拼多多": ("%s %s 工厂直发 特价包邮" % (core, pt2) if cat_in_core
                   else "%s %s 工厂直发 特价包邮 %s" % (core, pt2, cat)),
        "抖音":   "别再乱买%s了！%s真的绝，闭眼入" % (cat, pt2),
        "小红书": "挖到宝了！%s天花板｜%s" % (cat, pt2),
    }

    results = []
    for p in PLATFORMS:
        t = _cut(drafts[p["name"]], p["max"])
        results.append({
            "platform": p["name"],
            "title": t,
            "length": len(t),
            "max": p["max"],
            "style": p["style"],
            "banned": check_banned(t),
        })
    return results
