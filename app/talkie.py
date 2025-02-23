import yaml
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st

title = "Talkie Toaster 🚀"
model_name = "gemma2"
# deepseek-r1 was fun to watch, but had trash output
# gemma2 was surprisingly accurate but still off from event gpt-35-turbo
# qwem2 was too helpful, but good, didn't check accuracy
# llama3.2 was fast but just as flakey as gemma
# phi4 was slower but prone to hallucinations, between gemma and deepseek

st.set_page_config(page_title=title)
st.title(title)

with open("data/talkie.yml") as stream:
    config = yaml.safe_load(stream)

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    if (config):
        st.session_state["messages"].extend(config["messages"])

def sanitize_for_code(message):
    return {
        "role": message["role"],
        "content": message["content"].translate(str.maketrans({
            r"{": r"{{",
            r"}": r"}}",
            "-":  r"\-",
            "]":  r"\]",
            "\\": r"\\",
            "^":  r"\^",
            "$":  r"\$",
            "*":  r"\*",
            ".":  r"\.",
        }))
    }

messages = []
messages.extend(map(sanitize_for_code, st.session_state["messages"]))
messages.append({"role": "user", "content": "{prompt}"})
prompt = ChatPromptTemplate.from_messages(messages)
model = OllamaLLM(model=model_name)
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
