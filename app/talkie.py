import yaml
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st
from junk import sanitize_for_code

title = "Talkie Toaster 🚀"
model_name = "gemma2"
# deepseek-r1 was fun to watch, but had trash output
# gemma2 was surprisingly accurate but still off from event gpt-35-turbo
# qwem2 was too helpful, but good, didn't check accuracy
# llama3.2 was fast but just as flakey as gemma
# phi4 was slower but prone to hallucinations, between gemma and deepseek
config_files = [
    "data/quotes.yml",
    "data/talkie.yml",
]
chat_input_text = "Ask about anything but bready topics..."

st.set_page_config(page_title=title)
st.title(title)

chat_tab, system_tab = st.tabs(["Chat", "System"])

model_name = system_tab.text_input("model", model_name)
tempie = system_tab.slider("tempie", 0.0, 1.0, 1.0)
toppie = system_tab.slider("toppie", 0.0, 1.0, 1.0)
system_tab.markdown("## messages")
system_message_container = system_tab.container()
chat_container = chat_tab.container()

config = False
if "messages" not in st.session_state:
    config = { "messages": [] }
    for config_file in config_files:
        with open(config_file) as stream:
            yaml_config = yaml.safe_load(stream)
            if (yaml_config["messages"]):
                config["messages"].extend(yaml_config["messages"])

    st.session_state["messages"] = []
    if (config):
        st.session_state["messages"].extend(config["messages"])

messages = []
messages.extend(map(sanitize_for_code, st.session_state["messages"]))
messages.append({"role": "user", "content": "{prompt}"})
prompt = ChatPromptTemplate.from_messages(messages)
model = OllamaLLM(model=model_name, temperature=tempie, top_p=toppie)
chain = prompt | model

if config: # Run once on start
    response = chain.invoke({"prompt": "Greet me"})
    st.session_state["messages"].append(
        {"role": "assistant", "content": response})

for msg in st.session_state["messages"]:
    if (msg["role"] == "system"):
        system_message_container.chat_message(msg["role"]).write(msg["content"])
    else:
        chat_container.chat_message(msg["role"]).write(msg["content"])

if prompt := chat_tab.chat_input(placeholder=chat_input_text):
    chat_container.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    response = chain.invoke({"prompt": prompt})

    chat_container.chat_message("assistant").write(response)
    st.session_state["messages"].append(
        {"role": "assistant", "content": response})
