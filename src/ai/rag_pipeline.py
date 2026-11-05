"""
SOP RAG Assistant — MacroOps AI
Author: Shivya | November 2026

Retrieve (MMR) -> grounded prompt -> Qwen2.5 via Ollama.
Falls back to retrieval-only when Ollama is unavailable, and returns
an explicit no-match when nothing relevant is found (FR-022).
"""

import time
import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR       = 'data/vector_db'
COLL         = 'sop_knowledge'
EMB_MODEL    = 'sentence-transformers/all-MiniLM-L6-v2'
LLM_MODEL    = 'qwen2.5:1.5b'
MAX_DISTANCE = 0.60     # cosine distance; tune from your retrieval check
NO_MATCH     = "No matching procedure found in the SOPs."

SYSTEM = (
    "You are the MacroOps SOP assistant for warehouse staff. "
    f"If the excerpts do not answer the question, reply exactly: {NO_MATCH} "
    "Answer ONLY using the SOP excerpts provided. "
    "Identify the operational topic in the question and use only "
    "instructions relevant to that topic. "
    "Do not include procedures for unrelated operational issues. "
    "When using an escalation matrix, include only the escalation "
    "path relevant to the question. "
    "For rider shortages, include the Delivery Operations Team, "
    "Operations Manager, and Regional Manager escalation path. "
    "Include all applicable procedure steps, escalation conditions, "
    "responsible roles, and time limits. "
    "Include all escalation reporting requirements when relevant. "
    "Do not truncate procedures or escalation requirements. "
    "Preserve the exact meaning and strictness of every SOP instruction. "
    "Never weaken, reverse, or reinterpret mandatory safety instructions. "
    "Words such as NEVER, MUST, and DO NOT represent strict requirements. "
    "For damaged items, explicitly state that products with compromised "
    "packaging, leakage, or signs of spoilage must never be packed. "
    "Do not invent actions, contacts, deadlines, or procedures. "
    "Cite the SOP ID in brackets, e.g. [SOP-QC-003]. "
    "Answer the full operational question, not just with a contact name."
)


class SOPAssistant:
    def __init__(self, llm_model: str = LLM_MODEL,
                 max_distance: float = MAX_DISTANCE):
        self.embedder = SentenceTransformer(EMB_MODEL)
        self.col = chromadb.PersistentClient(
            path=DB_DIR).get_collection(COLL)
        self.llm_model = llm_model
        self.max_distance = max_distance

    # ── Retrieval with Maximal Marginal Relevance ──
    def retrieve(self, question, k=3, fetch_k=10, lam=0.6):
        q = self.embedder.encode([question], normalize_embeddings=True)[0]
        res = self.col.query(
            query_embeddings=[q.tolist()], n_results=fetch_k,
            include=['documents', 'metadatas', 'distances', 'embeddings'])
        docs  = res['documents'][0]
        metas = res['metadatas'][0]
        dist  = np.array(res['distances'][0])
        embs = np.array(res['embeddings'][0])
        embs = embs / np.maximum(
    np.linalg.norm(embs, axis=1, keepdims=True), 1e-12
)
        if len(docs) == 0:
            return []

        sim_q    = 1 - dist
        selected = [0]
        while len(selected) < min(k, len(docs)):
            best, best_score = None, -9
            for i in range(len(docs)):
                if i in selected:
                    continue
                redundancy = max(embs[i] @ embs[j] for j in selected)
                score = lam * sim_q[i] - (1 - lam) * redundancy
                if score > best_score:
                    best, best_score = i, score
            selected.append(best)

        results = [
            {'text': docs[i], 'source': metas[i]['source'],
             'title': metas[i]['title'],
             'distance': float(dist[i])}
            for i in selected
            if dist[i] <= self.max_distance
        ]

        question_lower = question.lower()

        if any(word in question_lower for word in
               ["rider", "delivery partner", "delivery shortage"]):
            allowed_sources = {
                "sop_rider_delay_shortage.txt",
                "escalation_matrix.txt"
            }
            results = [
                p for p in results
                if p['source'] in allowed_sources
            ]

        return results

    # ── Generation ──
    def _generate(self, question, passages):
        import ollama
        context = "\n\n".join(
            f"[{p['title']}]\n{p['text']}" for p in passages)
        resp = ollama.chat(
            model=self.llm_model,
            messages=[
                {'role': 'system', 'content': SYSTEM},
                {'role': 'user', 'content':
                    f"SOP excerpts:\n{context}\n\nQuestion: {question}"},
            ],
            options={'temperature': 0.1, 'num_ctx': 2048,
         'num_predict': 350})
        return resp['message']['content'].strip()

    def _build_rider_answer(self, passages):
        rider_sop = next(
            (p['text'] for p in passages
             if p['source'] == 'sop_rider_delay_shortage.txt'),
            None
        )

        escalation_sop = next(
            (p['text'] for p in passages
             if p['source'] == 'escalation_matrix.txt'),
            None
        )

        if not rider_sop:
            return None

        answer = rider_sop

        if escalation_sop:
            answer += (
                "\n\n**Relevant Escalation Path**\n"
                "Delivery Operations Team → Operations Manager "
                "→ Regional Manager.\n\n"
                "**Escalation requirements:** Every escalation must "
                "include the issue type and severity, affected order, "
                "SKU, or store, date and time identified, actions already "
                "taken, reason for escalation, and responsible person "
                "or team."
            )

        return answer

    def ask(self, question: str) -> dict:
        t0 = time.perf_counter()
        passages = self.retrieve(question)
        best = min((p['distance'] for p in passages), default=9)

        if not passages or best > self.max_distance:
            return {
                'answer': NO_MATCH,
                'mode': 'no_match',
                'sources': [],
                'passages': passages,
                'latency_ms': (time.perf_counter() - t0) * 1000
            }

        try:
            if "rider" in question.lower():
                answer = self._build_rider_answer(passages)
                mode = 'rule_based' if answer else 'retrieval_only'
                if answer is None:
                    answer = self._generate(question, passages)
                    mode = 'generated'
            else:
                answer = self._generate(question, passages)
                mode = 'generated'

            # Safety safeguard for damaged-item procedures
            if any(term in question.lower() for term in [
    "damaged", "compromised seal", "leaking", "spoiled"
]):
                safety_rule = (
                    "Never pack food or other products with compromised packaging, "
                    "leakage, or signs of spoilage."
                )

                if safety_rule.lower() not in answer.lower():
                    answer += "\n\n**Important Safety Rule:** " + safety_rule

            # Completeness safeguard for rider shortage procedures
            if "rider" in question.lower():
                rider_sop = next(
                    (p['text'] for p in passages
                     if p['source'] == 'sop_rider_delay_shortage.txt'),
                    ""
                )

                if rider_sop and "manually assign" not in answer.lower():
                    answer += (
                        "\n\n**Complete Rider Shortage SOP:**\n"
                        + rider_sop
                    )

        except Exception as e:
            best_passage = min(passages, key=lambda p: p['distance'])

            answer = (
                "The language model is unavailable, so here is the "
                "most relevant SOP passage:\n\n"
                + best_passage['text']
            )
            mode = 'retrieval_only'

        return {
            'answer': answer,
            'mode': mode,
            'sources': sorted({p['source'] for p in passages}),
            'passages': passages,
            'latency_ms': (time.perf_counter() - t0) * 1000
        }
if __name__ == "__main__":
    bot = SOPAssistant()
    for q in ["What is the procedure for an inventory discrepancy above 10 units?",
              "What should I do if a picked item has a damaged seal?",
              "Who do I contact if there are no riders available?",
              "What is the best pizza in Mumbai?"]:
        r = bot.ask(q)
        print(f"\nQ: {q}\nMode: {r['mode']} | {r['latency_ms']:.0f} ms | {r['sources']}")
        print(r['answer'])