import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Mera Mobile AI", page_icon="📱")
st.title("📱 Mera Apna AI Chatbot")
st.write("Yeh chatbot maine poora mobile se banaya hai!")

# Sidebar mein API Key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Apni API Key yahan dalein:", type="password")
    st.markdown("[OpenRouter](https://openrouter.ai/) se free key le sakte hain.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yahan kuch bhi type karein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        st.warning("Kripya pehle Sidebar mein apni API Key dalein!")
    else:
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response = client.chat.completions.create(
                    model="meta-llama/llama-3-8b-instruct:free",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                full_response = response.choices[0].message.content
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Galti hui: {e}")
