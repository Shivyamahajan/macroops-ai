"""Page 6: SOP Assistant (RAG) — MacroOps AI"""
import streamlit as st
import sys
sys.path.append('.')


@st.cache_resource
def get_sop():
    from src.ai.rag_pipeline import SOPAssistant
    return SOPAssistant()


def render(store_id: str = None):
    st.markdown('<div class="main-header">📚 SOP Assistant</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Procedure guidance for frontline '
                'staff, grounded in the SOP documents</div>',
                unsafe_allow_html=True)

    try:
        bot = get_sop()
    except Exception:
        st.error("Knowledge base not found. Run "
                 "`python src/ai/build_knowledge_base.py`.")
        return

    quick = ["What is the procedure for an inventory discrepancy above 10 units?",
             "What should I do if a picked item has a damaged seal?",
             "What do I do if I cannot find an item on the shelf?",
             "When should an order be escalated to the Regional Manager?"]
    cols = st.columns(len(quick))
    for c, qq in zip(cols, quick):
        if c.button(qq[:38] + "...", key=qq):
            st.session_state['sop_q'] = qq

    q = st.text_input("Ask a procedure question",
                      value=st.session_state.get('sop_q', ''))
    if st.button("Ask", type="primary") and q.strip():
        with st.spinner("Searching SOPs..."):
            r = bot.ask(q)

        if r['mode'] == 'no_match':
            st.warning(r['answer'])
        elif r['mode'] == 'retrieval_only':
            st.info("Language model offline. Showing the matching SOP text.")
            st.markdown(r['answer'])
        else:
            st.markdown(r['answer'])

        st.caption(f"Mode: {r['mode']} · {r['latency_ms']/1000:.1f}s"
                   + (f" · Sources: {', '.join(r['sources'])}"
                      if r['sources'] else ""))
        if r['passages']:
            with st.expander("Show retrieved SOP passages"):
                for p in r['passages']:
                    st.markdown(f"**{p['source']}** "
                                f"(distance {p['distance']:.2f})")
                    st.text(p['text'])
render()