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
    ('stockouts', r'stock.?out|out of stock|zero available inventory|zero inventory|no available inventory|completely out', T.stockouts),    ('slow_pickers',  r'(slow|worst|slowest|longest|highest).{0,30}picker|picker.{0,30}(slow|worst|longest|highest)|picker.{0,20}(picking )?times?.{0,20}(highest|longest)', T.slowest_pickers),
    ('avg_pick', r'average.{0,20}pick(ing)?.{0,20}(time|duration)|average.{0,20}(time|duration).{0,30}pick(ing)?|pick(ing)?.{0,15}(time|duration)|how long.{0,15}pick|how many minutes.{0,20}pick', T.avg_pick),    ('inv_stores',    r'inventory.{0,20}accuracy|accuracy.{0,20}inventory|lowest accuracy', T.low_inventory_stores),
    ('assignment', r'assignment|rider.{0,30}(delay|wait|assign)|delay.{0,30}rider|ready.{0,30}rider', T.assignment_delay),
    ('overloaded',    r'overload|pending tasks|workload', T.overloaded_stores),
    ('worst_stores',  r'(worst|poor|lowest|bottom|highest|top).{0,30}store|store.{0,30}(worst|poor|lowest|bottom|highest|top|breach rate)|which store', T.worst_stores),    ('store_summary', r'summary|overview|how is', T.store_summary),
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
    numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "nine": 9, "ten": 10
    }

    pattern = (
        r'\b(?:top|worst|best|bottom|slowest)?\s*'
        r'(?:the\s+)?(\d+|one|two|three|four|five|six|seven|'
        r'eight|nine|ten)\s+'
        r'(?:slowest|worst|best|highest|lowest)?\s*'
        r'(?:stores|pickers|orders)\b'
    )

    m = re.search(pattern, q, re.I)

    if not m:
        return default

    value = m.group(1).lower()
    n = int(value) if value.isdigit() else numbers[value]

    return max(1, min(n, 20))


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
            name, fn = next(
                ((i, f) for i, _p, f in INTENTS
                 if i == self.last_intent),
                (None, None)
            )

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