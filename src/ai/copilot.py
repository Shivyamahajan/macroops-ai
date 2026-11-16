"""
AI Operations Copilot — MacroOps AI
Author: Shivya | November 2026

Rule-based intent routing -> pandas tools -> templated answer.
Procedure questions go to the SOP RAG assistant.
Hybrid questions ("what should I do about slow picks?") get both.
"""

import re
import time
from src.ai import copilot_tools as T

# Order matters: more specific patterns first.
INTENTS = [
    ('at_risk',       r'at risk|risk of|likely to (breach|miss)|predicted|risky', T.at_risk_orders),
    ('exceptions',    r'exception', T.exception_counts),
    ('stockouts',     r'stock.?out|out of stock', T.stockouts),
    ('slow_pickers',  r'(slow|worst|slowest).{0,15}picker|picker.{0,15}(slow|worst)', T.slowest_pickers),
    ('avg_pick',      r'pick(ing)?\s+(time|duration)|how long.{0,15}pick', T.avg_pick),
    ('assignment',    r'assignment|rider.{0,20}(delay|wait)|delay.{0,20}rider', T.assignment_delay),
    ('inv_stores',    r'inventory.{0,20}accuracy|accuracy.{0,20}inventory|lowest accuracy', T.low_inventory_stores),
    ('overloaded',    r'overload|pending tasks|workload', T.overloaded_stores),
    ('worst_stores',  r'(worst|poor|lowest|bottom).{0,20}store|which store|store.{0,20}(worst|performing)', T.worst_stores),
    ('store_summary', r'summary|overview|how is', T.store_summary),
    ('breach',        r'\bsla\b|breach|on.?time', T.sla_breach),
]

PROCEDURAL = re.compile(
    r'\b(procedure|sop|policy|protocol|steps?|escalat\w*|'
    r'what should|what do i|how (do|should|to)|who (do|should|handles))\b',
    re.I)

SUGGESTIONS = ("I can answer questions about SLA breach rate, worst stores, "
               "slow pickers, picking time, rider assignment delay, "
               "stockouts, inventory accuracy, overloaded stores, "
               "exceptions, and at-risk orders, or look up an SOP.")


def _extract_n(q, default=5):
    m = (
        re.search(
            r'\b(?:top|worst|best|bottom|slowest)\s+(\d+)', q, re.I
        )
        or re.search(
            r'\b(\d+)\s+(?:slowest|worst|best)\s+(?:stores|pickers|orders)\b',
            q, re.I
        )
        or re.search(
            r'\b(\d+)\s+(?:stores|pickers|orders)\b', q, re.I
        )
    )
    return max(1, min(int(m.group(1)), 20)) if m else default


def _extract_store(q):
    m = re.search(r'\bST\s?-?(\d{1,3})\b', q, re.I)
    return f"ST{int(m.group(1)):03d}" if m else None


class OperationsCopilot:
    def __init__(self, sop_assistant=None):
        self.sop = sop_assistant
        self.last_intent = None
        self.history = []

    def _route(self, q):
        for name, pattern, fn in INTENTS:
            if re.search(pattern, q, re.I):
                return name, fn
        return None, None

    def ask(self, question: str) -> dict:
        t0 = time.perf_counter()
        store = _extract_store(question)
        n = _extract_n(question)
        name, fn = self._route(question)

        # light memory: "and for ST012?" reuses the previous intent
        if name is None and store and self.last_intent:
            name, fn = next((i, f) for i, _p, f in INTENTS
                            if i == self.last_intent), (None, None)
            name, fn = self.last_intent, fn

        parts, table, sources, mode = [], None, [], 'data'
        if fn:
            res = fn(store=store, n=n)
            parts.append(res['text'])
            table = res.get('table')
            if res.get('source'):
                sources.append(res['source'])
            self.last_intent = name

        use_sop = (PROCEDURAL.search(question) is not None) or fn is None
        if use_sop and self.sop is not None:
            r = self.sop.ask(question)
            if r['mode'] == 'no_match' and fn is None:
                parts.append(r['answer'] + " " + SUGGESTIONS)
                mode = 'no_answer'
            elif r['mode'] != 'no_match':
                parts.append("**Procedure:**\n" + r['answer'])
                sources += r['sources']
                mode = 'hybrid' if fn else 'sop'
        elif use_sop and fn is None:
            parts.append(SUGGESTIONS)
            mode = 'no_answer'

        out = {'answer': "\n\n".join(parts), 'table': table,
               'sources': sources, 'intent': name, 'mode': mode,
               'latency_ms': (time.perf_counter() - t0) * 1000}
        self.history.append({'q': question, **{k: out[k] for k in
                             ('answer', 'intent', 'mode')}})
        return out


if __name__ == "__main__":
    from src.ai.rag_pipeline import SOPAssistant
    bot = OperationsCopilot(SOPAssistant())
    for q in ["What is the SLA breach rate?",
              "Which 5 stores have the worst SLA performance?",
              "Who are the 3 slowest pickers?",
              "How is ST044 doing?",
              "What is the average assignment delay for ST098?",
              "Which SKUs are out of stock?",
              "What should I do about slow picking?",
              "What is the capital of France?"]:
        r = bot.ask(q)
        print(f"\nQ: {q}\n[{r['intent']} | {r['mode']} | {r['latency_ms']:.0f} ms]")
        print(r['answer'])
        if r['table'] is not None:
            print(r['table'].to_string(index=False))