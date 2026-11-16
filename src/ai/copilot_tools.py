"""
Copilot data tools — MacroOps AI
Author: Shivya | November 2026
All numbers are computed with pandas. The LLM never produces figures.
"""

import sys
import pandas as pd
sys.path.append('.')

_DATA = None


def data():
    global _DATA
    if _DATA is None:
        from src.analytics.load_data import load_all
        _DATA = load_all()
    return _DATA


def _store_orders(store):
    o = data()['orders']
    return o[o['store_id'] == store] if store else o


def _res(text, table=None, source=''):
    return {'text': text, 'table': table, 'source': source}


def sla_breach(store=None, **_):
    o = _store_orders(store)
    if o.empty:
        return _res(f"No orders found for {store}.", source='orders.csv')
    rate = o['sla_breached'].mean() * 100
    where = f" for {store}" if store else " across all stores"
    return _res(f"SLA breach rate{where}: {rate:.1f}% "
                f"({int(o['sla_breached'].sum()):,} of {len(o):,} orders).",
                source='orders.csv (sla_breached)')


def worst_stores(n=5, **_):
    o = data()['orders']
    t = (o.groupby('store_id')
           .agg(orders=('order_id', 'count'),
                breach_rate=('sla_breached', lambda x: x.mean() * 100))
           .round(1).sort_values('breach_rate', ascending=False)
           .head(n).reset_index())
    top = t.iloc[0]
    return _res(f"The {n} stores with the highest SLA breach rate are shown "
                f"below. Worst: {top['store_id']} at {top['breach_rate']}%.",
                t, 'orders.csv (sla_breached by store)')


def slowest_pickers(n=5, min_orders=10, **_):
    p = data()['picking']
    t = (p.groupby('picker_id')
           .agg(orders=('order_id', 'count'),
                avg_pick_min=('pick_duration_minutes', 'mean'))
           .query('orders >= @min_orders')
           .sort_values(['avg_pick_min', 'picker_id'],
             ascending=[False, True])
           .head(n).round(1).reset_index())
    return _res(f"The {n} slowest pickers by average pick time "
                f"(minimum {min_orders} orders) are shown below.",
                t, 'picking.csv (pick_duration_minutes)')


def avg_pick(store=None, **_):
    p, o = data()['picking'], data()['orders']
    if store:
        p = p[p['order_id'].isin(o[o['store_id'] == store]['order_id'])]
    if p.empty:
        return _res("No picking records for that selection.",
                    source='picking.csv')
    where = f" for {store}" if store else ""
    return _res(f"Average pick duration{where}: "
                f"{p['pick_duration_minutes'].mean():.1f} minutes; "
                f"{(p['pick_duration_minutes'] > 20).mean()*100:.1f}% of "
                f"picks exceed 20 minutes ({len(p):,} picks).",
                source='picking.csv (pick_duration_minutes)')


def assignment_delay(store=None, **_):
    d, o = data()['delivery'], data()['orders']
    if store:
        d = d[d['order_id'].isin(o[o['store_id'] == store]['order_id'])]
    if d.empty:
        return _res("No delivery records for that selection.",
                    source='delivery.csv')
    where = f" for {store}" if store else ""
    return _res(f"Average rider assignment delay{where}: "
                f"{d['assignment_delay_minutes'].mean():.1f} minutes; "
                f"{(d['assignment_delay_minutes'] > 15).mean()*100:.1f}% "
                f"of deliveries waited over 15 minutes ({len(d):,} deliveries).",
                source='delivery.csv (assignment_delay_minutes)')


def stockouts(store=None, **_):
    i = data()['inventory']
    if store:
        i = i[i['store_id'] == store]
    s = i[i['stockout'] == 'Yes'][['store_id', 'sku_id',
                                   'system_stock', 'physical_stock']]
    where = f" in {store}" if store else ""
    return _res(f"{len(s)} SKU-store combination(s) are completely out of "
                f"stock{where}.", s.reset_index(drop=True) if len(s) else None,
                'inventory.csv (stockout)')


def low_inventory_stores(n=5, **_):
    i = data()['inventory']
    t = (i.groupby('store_id')['inventory_accuracy_pct'].mean().round(1)
           .sort_values().head(n).reset_index()
           .rename(columns={'inventory_accuracy_pct': 'avg_accuracy_pct'}))
    return _res(f"The {n} stores with the lowest average inventory accuracy "
                f"are shown below. Lowest: {t.iloc[0]['store_id']} at "
                f"{t.iloc[0]['avg_accuracy_pct']}%.",
                t, 'inventory.csv (inventory_accuracy_pct)')


def overloaded_stores(n=5, **_):
    w = data()['workforce']
    t = (w.groupby('store_id')
           .agg(avg_pending=('tasks_pending', 'mean'),
                overloaded=('tasks_pending', lambda x: (x > 10).sum()))
           .round(2).sort_values('avg_pending', ascending=False)
           .head(n).reset_index())
    return _res(f"The {n} stores with the highest average pending tasks per "
                f"employee are shown below.",
                t, 'workforce.csv (tasks_pending)')


def exception_counts(store=None, **_):
    from src.analytics.exception_engine import detect_exceptions

    ex = detect_exceptions(limit=10**7)

    if store:
        ex = ex[ex['store_id'].astype(str).str.upper() == store.upper()]

    counts = ex['exception_type'].value_counts()
    t = pd.DataFrame({
        'type': counts.index,
        'count': counts.values
    })

    high = ex['severity'].isin(['High', 'Critical']).sum()
    medium = (ex['severity'] == 'Medium').sum()

    where = f" for {store}" if store else ""

    return _res(
        f"{len(ex):,} exceptions detected{where} "
        f"({high:,} high/critical, {medium:,} medium severity).",
        t if not t.empty else None,
        'exception_engine (rule-based)'
    )

def at_risk_orders(n=5, **_):
    try:
        from src.analytics.load_data import load_master
        from src.ai.feature_engineering import build_ml_table, time_split
        from src.ai.sla_predictor import SLAPredictor
        table, _f = build_ml_table(load_master())
        _a, _b, test = time_split(table)
        sc = SLAPredictor().score(test.tail(5000))
        t = (sc.sort_values('risk_probability', ascending=False)
               .head(n)[['order_id', 'store_id', 'risk_probability',
                         'risk_tier']].round(3).reset_index(drop=True))
        return _res(f"Top {n} orders by predicted breach risk "
                    f"(historical test-period orders scored in "
                    f"demonstration mode).", t, 'sla_model.pkl')
    except Exception as e:
        return _res(f"The SLA risk model is not available ({e}).",
                    source='sla_model.pkl')


def store_summary(store=None, **_):
    if not store:
        return _res("Please name a store, for example: summary for ST044.")
    parts = [sla_breach(store)['text'], avg_pick(store)['text'],
             assignment_delay(store)['text']]
    inv = data()['inventory']
    inv = inv[inv['store_id'] == store]
    if len(inv):
        parts.append(f"Average inventory accuracy: "
                     f"{inv['inventory_accuracy_pct'].mean():.1f}%.")
    return _res(" ".join(parts), source='orders, picking, delivery, inventory')