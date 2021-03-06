import streamlit as st
from PIL import Image
import requests
import io
from seaborn import barplot,set_theme,despine,set_style
import pandas as pd
import matplotlib.pyplot as plt
import webbrowser
import time

github_url = 'https://github.com/gregoirelafay/neural-art'


st.set_option("deprecation.showfileUploaderEncoding", False)
st.title('Neural Art')
logo_wagon = Image.open('wagon.png')
st.image(logo_wagon,width=75)

st.header("Let's play, can we predict  the Art Style of your painting ?")
st.markdown('Upload below an image, or take one with your phone')

uploaded_file = st.file_uploader("Choose an image", type= ['png','jpg','jpeg'])


if uploaded_file is not None:

    # uploaded_file.__dict__
    # uploaded_file

    image = Image.open(uploaded_file)
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        st.image(image, caption="Uploaded image", use_column_width='auto')

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

    st.markdown('Here is our prediction for your image')

    if response.status_code == 200:
        resp = response.json()
    else:
        "😬 api error 🤖"

    data = resp["pred"]

    data = eval(data)
    data = {i: j for i, j in data.items() if j > 0.01}
    data = pd.DataFrame(list(data.items()), columns=["Movement", "Prediction"])
    data.set_index("Movement")

    set_theme(style="darkgrid", palette="Set2", context="poster")
    set_style(style='white')

    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    barplot(data=data,
            y="Movement",
            x="Prediction",
            order=data.sort_values("Prediction", ascending=True).Movement,
            ax=ax,dodge=False)
    ax.set_ylabel("Art Style",
                  loc='top',
                  rotation='horizontal',
                  color="#FF4500")
    ax.set_xlabel('Prediction value (%)', color="#FF4500")
    ax.set_ylim((-2, 5))
    ax.spines["bottom"].set_color("#FF4500")
    ax.spines["left"].set_color("#FF4500")
    #ax.yaxis.label.set_color('#FF4500')
    ax.tick_params(axis='y', colors='#FF4500')

    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    despine()

    for i, v in enumerate(
        list(data.sort_values("Prediction", ascending=True).Prediction)):
        ax.text(v,
                i,
                "{0:.0%}".format(v),
                color='black',
                fontweight='bold',
                horizontalalignment='right')

    st.pyplot(fig, transparent=True,)

st.text("")
st.text("")
st.text("")
check1 = st.button("Explanations")


if check1:
    st.markdown("Context for your prediction:")
    st.markdown("   - We collected a dataset (thanks WikiArt) of 40.000 images split in 8 different Art Styles (class):")
    st.markdown("       - Our input (X) is strictly images ! ")
    st.markdown("       - you can find below the split between our 8 class")
    split_movement_png = Image.open('class_split_2.png')
    st.image(split_movement_png, use_column_width=True)
    st.markdown("   - We trained a custom Convolutional Neural Network Models (see our repo on github)")
    st.markdown("       - Our output (Y) is probability number for our 8 different Art Styles")
    st.markdown("       - That's why you may see multiple predicions for your painting")

st.text("")
st.markdown('Like it ? Want to know more ? Click below')

if st.button('View Source Code on Github'):
    webbrowser.open_new_tab(github_url)
