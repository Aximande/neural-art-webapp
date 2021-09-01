import streamlit as st
from PIL import Image
import requests
import io
from seaborn import barplot,set_theme,despine
import pandas as pd
import matplotlib.pyplot as plt

st.set_option("deprecation.showfileUploaderEncoding", False)
uploaded_file = st.file_uploader("Choose an image", type= ['png','jpg','jpeg'])

if uploaded_file is not None:

    # uploaded_file.__dict__
    # uploaded_file

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=False)

    # convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG') #to-do: take as well jpg
    img_byte_arr = img_byte_arr.getvalue()

    # with open("image.jpg", "wb") as f:
    #     f.write(img_byte_arr)

    # api call
    #url = "http://localhost:8080/uploadfile" #to check when running in local
    url = 'https://neural-art-ympziugdca-nw.a.run.app/uploadfile'
    files = {"file": img_byte_arr}

    response = requests.post(url, files=files)

    if response.status_code == 200:
        resp = response.json()
    else:
        "😬 api error 🤖"

    data = resp["pred"]

    data = eval(data)
    data = {i: j for i, j in data.items() if j > 0.1}
    data = pd.DataFrame(list(data.items()), columns=["Movement", "Prediction"])
    data.set_index("Movement")

    set_theme(style="darkgrid", palette="Set2", context="poster")

    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    barplot(data=data,
            y="Movement",
            x="Prediction",
            order=data.sort_values("Prediction", ascending=False).Movement,
            ax=ax)
    ax.set_ylabel("Art Style")
    despine()

    for i, v in enumerate(
        list(data.sort_values("Prediction", ascending=False).Prediction)):
        ax.text(v, i, "{0:.0%}".format(v), color='black', fontweight='bold')
