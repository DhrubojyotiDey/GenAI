from dotenv import load_dotenv
load_dotenv()


import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key='Your_API_key')

model=genai.GenerativeModel("gemini-pro")
def get_response(query):
    response=model.generate_content(query)
    return response.text


st.set_page_config(page_title="Q&A page")

st.header("Gemini app")

input=st.text_input("Input: ", key="input")
submit=st.button("ask")

if submit:
    response=get_response(input)
    st.subheader("The response is ")
    st.write(response)

