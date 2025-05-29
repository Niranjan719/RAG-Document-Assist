from jinja2.compiler import generate
from typing import Set
from backend.core import run_llm
import streamlit as st


st.header("Document Helper BOT")


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

prompt = st.text_input("User Prompt", placeholder="Enter your query....")
if prompt:
    with st.spinner("Generating response ... "):
        generated_response = run_llm(query=prompt)
        sources = set([doc.metadata["source"] for doc in generated_response["source_documents"]])

        formatted_response = (
            f"{generated_response['result']} \n\n {create_sources_string(sources)}"
        )



