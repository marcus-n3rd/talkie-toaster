import yaml
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st

st.title("Talkie Toaster 🚀")

with open("data/talkie.yml") as stream:
    config = yaml.safe_load(stream)

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    if (config):
        st.session_state["messages"].extend(config["messages"])

messages = []
messages.extend(st.session_state["messages"])
messages.append({"role": "user", "content": "{prompt}"})
prompt = ChatPromptTemplate.from_messages(messages)
model = OllamaLLM(model="gemma2")
chain = prompt | model

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    response = chain.invoke({"prompt": prompt})

    st.chat_message("assistant").write(response)
    st.session_state["messages"].append(
        {"role": "assistant", "content": response})
