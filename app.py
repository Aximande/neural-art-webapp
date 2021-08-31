import streamlit as st
from PIL import Image
import requests
import io

st.set_option("deprecation.showfileUploaderEncoding", False)
uploaded_file = st.file_uploader("Choose an image", type="png")

if uploaded_file is not None:

    # uploaded_file.__dict__
    # uploaded_file

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

    # convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG') #to-do: take as well jpg
    img_byte_arr = img_byte_arr.getvalue()

    # with open("image.jpg", "wb") as f:
    #     f.write(img_byte_arr)

    # api call
    url = "http://localhost:8080/uploadfile"
    files = {"file": img_byte_arr}

    response = requests.post(url, files=files)

    if response.status_code == 200:
        resp = response.json()
        resp
    else:
        "😬 api error 🤖"
