# from typing import Set
# from backend.core import run_llm
# import streamlit as st
#
#
# st.header("Document Helper BOT")
# prompt = st.text_input("User Prompt", placeholder="Enter your query....")
#
#
# def create_sources_string(source_urls: Set[str]) -> str:
#     if not source_urls:
#         return ""
#     sources_list = list(source_urls)
#     sources_list.sort()
#     sources_string = "sources:\n"
#     for i, source in enumerate(sources_list):
#         sources_string += f"{i+1}. {source}\n"
#     return sources_string
#
#
# if (
#     "chat_answers_history" not in st.session_state
#     and "user_prompt_history" not in st.session_state
#     and "chat_history" not in st.session_state
# ):
#     st.session_state["chat_answers_history"] = []
#     st.session_state["user_prompt_history"] = []
#     st.session_state["chat_history"] = []
#
# if prompt:
#     with st.spinner("Generating response ... "):
#         generated_response = run_llm(
#             query=prompt, chat_history=st.session_state["chat_history"]
#         )
#         sources = set(
#             [doc.metadata["source"] for doc in generated_response["source_documents"]]
#         )
#
#         formatted_response = (
#             f"{generated_response['result']} \n\n {create_sources_string(sources)}"
#         )
#
#         st.session_state["user_prompt_history"].append(prompt)
#         st.session_state["chat_answers_history"].append(formatted_response)
#         st.session_state["chat_history"].append(("human", prompt))
#         st.session_state["chat_history"].append(("ai", generated_response["result"]))
#
#         if st.session_state["chat_answers_history"]:
#             for generated_response, user_query in zip(
#                 st.session_state["chat_answers_history"],
#                 st.session_state["user_prompt_history"],
#             ):
#                 st.chat_message("user").write(user_query)
#                 st.chat_message("assistant").write(generated_response)

from typing import Set
from backend.core import run_llm
import streamlit as st

# Set page config for a better UI
st.set_page_config(page_title="Document Helper BOT", page_icon="🤖", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f4f6f8;
            padding: 1.5rem;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            color: #000000;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #d3d3d3;
        }
        .message.user {
            background-color: #d0ebff;
            color: #003366;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .message.bot {
            background-color: #e6ffe6;
            color: #003300;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .source-links {
            font-size: 0.85rem;
            color: #666666;
            margin-top: 0.5rem;
        }
        .header-title {
            font-size: 2.5rem;
            color: #003366;
            text-align: center;
            font-weight: bold;
            margin-bottom: 2rem;
        }
        .chat-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title Header
st.markdown('<div class="header-title">📄 Document Helper BOT</div>', unsafe_allow_html=True)

# Prompt Input
prompt = st.text_input("", placeholder="Ask something about your documents...")

# Helper to format sources
def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "<div class='source-links'><strong>Sources:</strong><ul>"
    for source in sources_list:
        sources_string += f"<li>{source}</li>"
    sources_string += "</ul></div>"
    return sources_string

# Initialize session state
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

# Chat processing
if prompt:
    with st.spinner("🤖 Thinking..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

# Display Chat History
if st.session_state["chat_answers_history"]:
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        ):
            st.markdown(f'<div class="message user">👤 {user_query}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="message bot">🤖 {generated_response}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # small change

