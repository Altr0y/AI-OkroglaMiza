import streamlit as st
import requests
import os

# Osnovne nastavitve
st.set_page_config(page_title="AI okrogla miza", layout="wide")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

st.title("🤖 AI Okrogla Miza")

# 1. Pridobivanje podatkov
@st.cache_data(show_spinner=False)
def fetch_agents():
    try:
        return requests.get(f"{BACKEND_URL}/api/list-agents", timeout=5).json()
    except:
        return []

agents = fetch_agents()

# 2. Stranski meni (Side-bar)
if not agents:
    st.sidebar.error("Napaka: Backend ni dosegljiv.")
    selected_ids = []
else:
    selected_ids = st.sidebar.multiselect(
        "Izberi agente za debato:",
        options=[a["id"] for a in agents],
        default=[agents[0]["id"]] if agents else [],
        format_func=lambda x: next(a["name"] for a in agents if a["id"] == x) #izpiše ime vsakega agenta glede na id
    )

# 3. Vnosno polje
user_input = st.chat_input("Vprašaj agente nekaj...")

# 4. Logika odgovarjanja
if user_input:
    if not selected_ids:
        st.warning("Najprej izberi vsaj enega agenta na levi.")
    else:
        # Priprava prostora za odgovore (stolpci)
        cols = st.columns(len(selected_ids))
        
        with st.spinner("Agenti pišejo..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/chat",
                    json={"agent_ids": selected_ids, "prompt": user_input}
                ).json()

                for idx, aid in enumerate(selected_ids):
                    with cols[idx]:
                        agent_data = res.get(aid, {})
                        st.subheader(agent_data.get("name", aid))
                        
                        text = agent_data.get("text", "Napaka pri odgovoru.")
                        
                        # Preprost prikaz brez kompleksnega parsanja
                        if "<thinking>" in text:
                            parts = text.split("</thinking>")
                            with st.expander("Razmišljanje..."):
                                st.write(parts[0].replace("<thinking>", "").strip())
                            st.write(parts[1].strip())
                        else:
                            st.write(text)
            except Exception as e:
                st.error(f"Povezava ni uspela: {e}")