import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession
import os
import google.auth

# key_path = "geminiexplorer-435216-99ffc4cefa37.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
# credentials, project_id = google.auth.default()
# print(credentials)

project = "geminiexplorer-435216"
vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)
chat = model.start_chat()
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text
    
    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role":"model",
            "content": output
        }
    )

st.title("Gemini Explorer")

if "messages" not in st.session_state:
    st.session_state.messages = []

for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message["role"],
        parts = [Part.from_text(message["content"])]
    )
    
    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    chat.history.append(content)

if len(st.session_state.messages) == 0:
    initial_prompt = "What is red?"
    llm_function(chat, initial_prompt)


query = st.chat_input("Gemini Explorer")
if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)