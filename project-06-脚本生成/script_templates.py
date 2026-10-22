# -*- coding: utf-8 -*-
"""短视频 / 直播脚本模板生成（演示模式）。

设计原则（面试可讲）：
- 脚本结构方法论沉淀为模板：短视频「钩子-共鸣-卖点-行动」四段式，直播「开场-过款-逼单」三段式；
- 结构确定（规则），内容可升级：接入大模型可按品类风格改写台词。
"""


def _points(points):
    ps = [p.strip() for p in (points or "").replace("，", ",").replace("、", ",").split(",") if p.strip()]
    return ps or ["大容量", "百搭", "耐磨"]


def demo_generate(product, points, price, audience):
    pt = _points(points)
    p1, p2, p3 = (pt + ["质感好", "性价比高"])[:3]
    aud = (audience or "").strip() or "20-35 岁通勤女生"
    prd = (product or "").strip() or "托特包"
    price = (str(price) or "").strip() or "129"

    videos = [
        {
            "name": "版本 A · 痛点开场",
            "beats": [
                {"time": "0-3s",  "type": "钩子",     "line": "还在为%s不够用换包发愁？" % p1, "shot": "特写：塞满的旧包，拉链卡住"},
                {"time": "3-10s", "type": "共鸣",     "line": "通勤、逛街、短途出游，一个包全搞定", "shot": "三场景快切：地铁/商场/车站"},
                {"time": "10-25s", "type": "卖点展示", "line": "%s｜%s｜%s，%s都说实用" % (p1, p2, p3, aud), "shot": "演示装下 13 寸电脑+水杯+化妆包"},
                {"time": "25-30s", "type": "行动号召", "line": "今天直播间只要 %s，点击下方小黄车" % price, "shot": "价格弹出 + 箭头指引"},
            ],
        },
        {
            "name": "版本 B · 悬念开场",
            "beats": [
                {"time": "0-3s",  "type": "钩子",     "line": "为什么这款%s回头率这么高？" % prd, "shot": "街拍背影，路人回头"},
                {"time": "3-10s", "type": "悬念铺垫", "line": "关键是%s还%s" % (p1, p2), "shot": "慢镜头开包展示内仓"},
                {"time": "10-25s", "type": "卖点展示", "line": "%s不心疼，%s 元拿下" % (p3, price), "shot": "对比同款大牌价格"},
                {"time": "25-30s", "type": "行动号召", "line": "点关注不迷路，评论区扣 1 发链接", "shot": "博主指向评论区"},
            ],
        },
    ]

    voiceover = (
        "%s们注意了！如果你也需要一只能装又好看的%s，今天这款一定要看完。"
        "第一，%s，13 寸电脑、水杯、化妆包一起塞；第二，%s，通勤约会都能背；"
        "第三，%s，日常刮蹭不心疼。现在下单只要 %s 元，点击小黄车，库存不多先到先得。"
        % (aud, prd, p1, p2, p3, price)
    )

    live = {
        "开场欢迎": "欢迎新进直播间的宝子们！今天专场是%s，%s闭眼入，先扣个 1 让我看看人数。" % (prd, aud),
        "过款介绍": "来，看这款：%s、%s、%s。我直接给你们演示——电脑、水杯、伞全部装进去还有空间。官方价 299，今天直播间 %s。" % (p1, p2, p3, price),
        "逼单节奏": "这个价格仅限今天直播间，库存最后 80 单，拍下 48 小时内发货，7 天无理由，不合适退回来运费险出。",
    }

    return {
        "videos": videos,
        "voiceover": voiceover,
        "live": live,
        "mode": "演示模式（结构模板生成；接入大模型可按品类风格改写台词）",
    }
