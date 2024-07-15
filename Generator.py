import os
import streamlit as st
import requests
import io
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Text to Image", page_icon="🖼️")

# Sidebar for Instructions and Credits
with st.sidebar:
    st.header("Instructions")
    st.write("1. Enter a text prompt in the input box.")
    st.write("2. Click 'Generate Image' to see the output.")
    st.write("3. The generated image will appear on the right.")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("Created by Himanshu Mali")

st.title('Text to Image Generator with AI')  # Title of the webpage

API_URL1 = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"  # API calling
API_URL2 = "https://api-inference.huggingface.co/models/hakurei/waifu-diffusion"  # Another API calling
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}"}  # Use environment variable for API Token

# Function to check if the image is correct
def query(payload):
    response1 = requests.post(API_URL1, headers=headers, json=payload)
    response2 = requests.post(API_URL2, headers=headers, json=payload)
    if response2.status_code == 200:  # 200 is the universal code which represents perfect working image
        return response2.content
    elif response1.status_code == 200:  # If the first URL is not working call the 2nd URL
        return response1.content
    else:
        return None  # If both URLs are not working return None

# Layout: Columns for input and output
col1, col2 = st.columns(2)

with col1:
    image_text = st.text_input("Enter text for image:", "")  # Taking input from user
    generate_button = st.button("Generate Image")  # Created button

with col2:
    if generate_button:  # If the button is clicked generate image
        with st.spinner('Generating image...'):
            image_bytes = query({"inputs": image_text})  # calling query function
            if image_bytes:
                try:
                    image = Image.open(io.BytesIO(image_bytes))  # Opening image using PIL
                    st.image(image)
                except Image.UnidentifiedImageError:
                    st.error("Cannot display image")
            else:
                st.error("No image bytes received.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.write("This is a text-to-image generator in which the user provides a text prompt, and an image is created using AI.<br>Integration is done using Hugging Face API.", unsafe_allow_html=True)
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
