import streamlit as st
import requests
import io
from PIL import Image

st.title('Text to Image') #Title of webpage

API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4" #API calling
headers = {"Authorization": "Bearer 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"} #API Token code

#Function to check if image is correct
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200: #200 is universal code which represents perfect working image
        return response.content
    else:
        return None

image_text = st.text_input("Enter text for image:", "") #Taking input from user

if st.button("Generate Image"):
    image_bytes = query({"inputs": image_text}) #calling query function
    if image_bytes:
        try:
            image = Image.open(io.BytesIO(image_bytes)) #Opening image using PIL
            st.image(image)
        except Image.UnidentifiedImageError:
            st.error("Cannot display image")
    else:
        st.error("No image bytes received.")
