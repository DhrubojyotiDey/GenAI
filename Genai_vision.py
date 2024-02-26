from dotenv import load_dotenv
load_dotenv()


import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key='Your_API_key')

model=genai.GenerativeModel("gemini-pro-vision")
def get_response(input, query):
    if input!="":
        response=model.generate_content([input, query])
    else:
        response=model.generate_content(query)
    return response.text


st.set_page_config(page_title="Q&A page")

st.header("Gemini app")

input=st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("your image: ", type=["jpg", "jpeg", "png"])

image=""

if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the picture")

#response=get_response(input, image)

if submit:
    response=get_response(input, image)
    st.subheader("The response is ")
    st.write(response)


