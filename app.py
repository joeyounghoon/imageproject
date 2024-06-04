import streamlit as st
import openai
from PIL import Image
import requests
from io import BytesIO

# Streamlit 애플리케이션 구성
st.title("AI Image Colorizer")
st.write("Upload a black-and-white PNG or JPG image and get a colorized version using OpenAI API.")

# OpenAI API 키 입력
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# 파일 업로드
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # 이미지 색칠하는 함수
    def colorize_image(image):
        # 이미지 바이너리를 OpenAI API로 전송
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = buffered.getvalue()
        
        response = openai.Image.create(
            prompt="colorize this image",
            image=img_str,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        
        # URL에서 이미지를 로드하여 반환
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        return img
    
    # 색칠된 이미지 출력
    if st.button("Colorize Image"):
        openai.api_key = api_key
        colorized_image = colorize_image(image)
        st.image(colorized_image, caption="Colorized Image", use_column_width=True)
