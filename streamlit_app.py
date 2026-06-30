import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Football Analyzer",
    page_icon="⚽",
)

st.title("⚽ Football Analyzer")

question = st.text_input(
    "Ask a football question", placeholder="Who is Cristiano Ronaldo?"
)

if st.button("Search"):
    if question:
        with st.spinner("Analyzing..."):
            start = time.perf_counter()
            response = requests.post(
                "http://127.0.0.1:8000/analyse", json={"question": question}
            )

            if response.status_code == 200:
                answer = response.text
                elapsed = time.perf_counter() - start

                st.write(answer)
                st.caption(f"⏱️ Response Time: {elapsed:.2f} sec")
            else:
                st.error("Something went wrong.")
