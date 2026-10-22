# 评价分析模块（规则版，无需大模型也能跑）
# 功能：情感分类 + 差评归因 + 改进建议映射
import csv, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(BASE, "sample_reviews.csv")

# 差评归因关键词（示例：包包类目，可替换）
CATEGORIES = {
    "质量": ["掉皮", "开裂", "破损", "开线", "脱胶", "五金", "掉色", "瑕疵",
             "做工", "走线", "拉链", "皮料", "味道", "气味", "变形", "压"],
    "物流": ["物流", "快递", "发货慢", "等了", "压变形", "盒子瘪", "收到"],
    "尺寸": ["太小", "太大", "尺寸", "装不下", "容量", "比想象", "肩带", "自重", "小很多"],
    "色差": ["色差", "颜色", "图片", "实物", "偏暗", "偏"],
    "服务": ["客服", "回复", "态度", "售后", "退款", "退换", "不回", "备注漏", "体验"],
}

POS = ["喜欢", "好看", "满意", "质量好", "推荐", "值", "不错", "百搭", "细致",
       "精致", "方便", "实惠", "友好", "在线", "用心", "面子", "整齐", "顺利"]
NEG = ["差", "坏", "失望", "后悔", "退", "问题", "不行", "丑", "慢", "瘪", "无语",
       "亏", "瑕疵", "开线", "掉色", "压变形", "不回", "介意", "瘪了", "心疼"]

# 归因 → 给运营的具体改进动作
IMPROVE = {
    "质量": ["加强出厂质检与皮料说明", "提供质保/保修说明",
             "拉链、五金等高风险工艺升级供应商"],
    "物流": ["升级合作快递并承诺发货时效", "加固包装防压变形",
             "偏远地区时效提前提醒"],
    "尺寸": ["详情页增加尺寸装物示意与自重标注", "写清肩带可调范围",
             "用视频展示真实大小"],
    "色差": ["自然光实拍并提示屏幕色差", "提供多光源色卡对比"],
    "服务": ["售前话术标准化与响应 SLA", "退换流程前置到详情页",
             "客服不回时自动兜底回复"],
}


def load_sample():
    rows = []
    with open(SAMPLE, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append(r["text"])
    return rows


def sentiment(text):
    score = 0
    for w in POS:
        if w in text:
            score += 1
    for w in NEG:
        if w in text:
            score -= 1
    if score > 0:
        return "正面"
    if score < 0:
        return "负面"
    return "中性"


def attribute(text):
    hits = [cat for cat, kws in CATEGORIES.items() if any(k in text for k in kws)]
    return hits or ["其他"]


def analyze(reviews):
    sent = Counter()
    attr = Counter()
    negative = []
    for t in reviews:
        s = sentiment(t)
        sent[s] += 1
        cats = attribute(t)
        for c in cats:
            attr[c] += 1
        if s == "负面":
            negative.append({"text": t, "cats": cats})

    improve = []
    for cat, cnt in attr.most_common():
        if cat in IMPROVE and cnt > 0:
            improve.append({"cat": cat, "count": cnt, "tips": IMPROVE[cat]})

    return {
        "total": len(reviews),
        "sentiment": dict(sent),
        "attribute": dict(attr),
        "negative": negative,
        "improve": improve,
    }
