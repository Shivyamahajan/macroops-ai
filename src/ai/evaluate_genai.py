
"""
GenAI evaluation harness — MacroOps AI
Author: Shivya | November 2026

Step 1:  python src/ai/evaluate_genai.py run
         -> runs all questions and saves reports/genai_eval_raw.csv

Step 2:  Grade the answers manually:
         correct      answer is factually right (1/0)
         grounded     claims are supported by the source (1/0)
         hallucinated answer contains unsupported information (1/0)

Step 3:  python src/ai/evaluate_genai.py score
"""

import sys
import pandas as pd

sys.path.append('.')

Q_FILE = 'tests/genai_eval_questions.csv'
RAW = 'reports/genai_eval_raw.csv'


def run():
    from src.ai.rag_pipeline import SOPAssistant
    from src.ai.copilot import OperationsCopilot

    sop = SOPAssistant()
    cop = OperationsCopilot(sop)

    qs = pd.read_csv(Q_FILE).fillna('')
    rows = []

    for _, q in qs.iterrows():
        if q['type'] == 'sop':
            r = sop.ask(q['question'])

            hit = (
                q['expected_source'] in r['sources']
                if q['expected_source'] != 'NONE'
                else r['mode'] == 'no_match'
            )

            rows.append({
                **q,
                'answer': r['answer'],
                'table': '',
                'mode': r['mode'],
                'sources': ';'.join(r['sources']),
                'retrieval_hit': int(hit),
                'latency_s': round(r['latency_ms'] / 1000, 2)
            })

        else:
            cop.last_intent = None
            r = cop.ask(q['question'])

            rows.append({
    **q,
    'answer': r['answer'],
    'table': (
        r['table'].to_csv(index=False)
        if r.get('table') is not None
        else ''
    ),
    'mode': r['mode'],
    'sources': ';'.join(r['sources']),
    'retrieval_hit': '',
    'latency_s': round(r['latency_ms'] / 1000, 2)
})

        print(
            q['id'],
            rows[-1]['mode'],
            rows[-1]['latency_s'],
            's'
        )

    df = pd.DataFrame(rows)

    for c in ['correct', 'grounded', 'hallucinated']:
        df[c] = ''

    df.to_csv(RAW, index=False)

    print(f"\nSaved {RAW}.")
    print("Fill correct/grounded/hallucinated manually, then run: score")


def score():
    df = pd.read_csv(RAW)

    graded = df.dropna(
        subset=['correct', 'grounded', 'hallucinated']
    )

    if len(graded) < len(df):
        print(
            f"Warning: only {len(graded)} of {len(df)} rows graded."
        )

    sop = df[
        (df['type'] == 'sop')
        & df['retrieval_hit'].notna()
    ]

    metrics = {
        'Questions evaluated': len(graded),
        'Answer accuracy (%)':
            graded['correct'].astype(float).mean() * 100,
        'Groundedness (%)':
            graded['grounded'].astype(float).mean() * 100,
        'Hallucination rate (%)':
            graded['hallucinated'].astype(float).mean() * 100,
        'Retrieval relevance, SOP (%)':
            sop['retrieval_hit'].astype(float).mean() * 100,
        'Mean response time (s)':
            df['latency_s'].mean(),
        'Responses under 5 s (%)':
            (df['latency_s'] < 5).mean() * 100,
    }

    targets = {
        'Answer accuracy (%)': '> 90',
        'Groundedness (%)': '> 95',
        'Hallucination rate (%)': '< 5',
        'Retrieval relevance, SOP (%)': '> 90',
        'Mean response time (s)': '< 5'
    }

    print(f"\n{'Metric':36s}{'Result':>10s}   Target")

    for key, value in metrics.items():
        print(
            f"{key:36s}{value:10.1f}   "
            f"{targets.get(key, '')}"
        )


if __name__ == "__main__":
    commands = {'run': run, 'score': score}

    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        print("Usage: python src/ai/evaluate_genai.py [run|score]")
        sys.exit(1)

    commands[sys.argv[1]]()
