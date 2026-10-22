# -*- coding: utf-8 -*-
"""经营数据日报分析器：纯规则实现，零依赖、可解释、可审计。

设计原则（面试可讲）：
- 环比与阈值检测用确定性规则 —— 可解释、零成本、可审计；
- 建议映射表用业务规则沉淀 —— 一换配置即可适配其他类目；
- 如需口语化润色日报，可复用项目一/二的大模型接入方式（可选增强）。
"""
import csv
import os

SAMPLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")

# 异常检测阈值（可按类目与店铺体量调整）
TH = {"traffic": 0.30, "refund": 0.08, "cr_drop": 0.25}


def load_sample():
    with open(SAMPLE, encoding="utf-8-sig") as f:  # utf-8-sig 兼容带 BOM 的导出文件
        return [dict(r) for r in csv.DictReader(f)]


def _num(rows):
    data = []
    for r in rows:
        data.append({
            "date": r.get("日期") or r.get("date") or "",
            "uv": float(r.get("访客数") or r.get("uv") or 0),
            "pv": float(r.get("浏览量") or r.get("pv") or 0),
            "buyers": float(r.get("支付买家数") or r.get("buyers") or 0),
            "gmv": float(r.get("支付金额") or r.get("gmv") or 0),
            "refund": float(r.get("退款金额") or r.get("refund") or 0),
            "cart": float(r.get("加购人数") or r.get("cart") or 0),
            "fav": float(r.get("收藏人数") or r.get("fav") or 0),
        })
    for d in data:
        d["cr"] = d["buyers"] / d["uv"] if d["uv"] else 0
        d["aov"] = d["gmv"] / d["buyers"] if d["buyers"] else 0
        d["refund_rate"] = d["refund"] / d["gmv"] if d["gmv"] else 0
    return data


def _pct(cur, prev):
    if not prev:
        return 0.0
    return (cur - prev) / prev


def analyze(rows):
    data = _num(rows)
    if len(data) < 2:
        return {"summary": {}, "changes": {}, "alerts": [],
                "daily_text": "数据不足两天的，无法计算环比，请至少提供两天数据。"}

    last, prev = data[-1], data[-2]
    changes = {
        "uv": round(_pct(last["uv"], prev["uv"]) * 100, 1),
        "gmv": round(_pct(last["gmv"], prev["gmv"]) * 100, 1),
        "cr": round(_pct(last["cr"], prev["cr"]) * 100, 1),
    }

    # 1) 异常检测：流量骤变
    alerts = []
    for i in range(1, len(data)):
        d, p = data[i], data[i - 1]
        uv_chg = _pct(d["uv"], p["uv"])
        if abs(uv_chg) >= TH["traffic"]:
            if uv_chg < 0:
                alerts.append({
                    "date": d["date"], "level": "warn", "metric": "访客数",
                    "detail": "骤降 %.1f%%（%d→%d）" % (abs(uv_chg * 100), p["uv"], d["uv"]),
                    "suggestion": "优先排查：搜索排名是否下滑、投放计划是否暂停、竞品大促是否分流",
                })
            else:
                alerts.append({
                    "date": d["date"], "level": "info", "metric": "访客数",
                    "detail": "激增 %.1f%%（%d→%d）" % (uv_chg * 100, p["uv"], d["uv"]),
                    "suggestion": "确认是否活动/短视频带动，复盘该渠道 ROI，评估能否常态化复制",
                })
        # 2) 退款率警戒线
        if d["gmv"] and d["refund_rate"] >= TH["refund"]:
            alerts.append({
                "date": d["date"], "level": "warn", "metric": "退款率",
                "detail": "%.1f%% 超过 %.0f%% 警戒线" % (d["refund_rate"] * 100, TH["refund"] * 100),
                "suggestion": "抽查当日退款原因 TOP3（质量/尺码/色差），同步调整详情页说明与客服话术",
            })

    # 3) 转化率异常（仅看最近一天）
    if prev["uv"] and _pct(last["cr"], prev["cr"]) <= -TH["cr_drop"]:
        alerts.append({
            "date": last["date"], "level": "warn", "metric": "支付转化率",
            "detail": "环比下降 %.1f%%" % abs(changes["cr"]),
            "suggestion": "检查价格竞争力、新增差评、详情页是否被竞品比价",
        })

    last7 = data[-7:]
    summary = {
        "date": last["date"],
        "gmv": round(last["gmv"]), "uv": int(last["uv"]), "buyers": int(last["buyers"]),
        "cr": round(last["cr"] * 100, 2), "aov": round(last["aov"]),
        "refund_rate": round(last["refund_rate"] * 100, 1),
        "gmv7": round(sum(d["gmv"] for d in last7)),
        "cr7": round(sum(d["buyers"] for d in last7) / max(sum(d["uv"] for d in last7), 1) * 100, 2),
    }

    # 4) 日报文本（规则模板，可解释）
    lines = [
        "【%s 经营日报】" % summary["date"],
        "昨日 GMV %d 元（环比 %+.1f%%），访客 %d（环比 %+.1f%%），转化率 %.2f%%，客单价 %d 元，退款率 %.1f%%。"
        % (summary["gmv"], changes["gmv"], summary["uv"], changes["uv"], summary["cr"], summary["aov"], summary["refund_rate"]),
        "近 7 天 GMV 合计 %d 元，平均转化率 %.2f%%。" % (summary["gmv7"], summary["cr7"]),
    ]
    if alerts:
        lines.append("异常与建议：")
        for a in alerts:
            lines.append("- %s %s%s → %s" % (a["date"], a["metric"], a["detail"], a["suggestion"]))
    else:
        lines.append("昨日无异常波动，维持现有投放与内容节奏即可。")
    return {"summary": summary, "changes": changes, "alerts": alerts, "daily_text": "\n".join(lines)}
