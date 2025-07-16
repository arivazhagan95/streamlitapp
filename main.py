import streamlit as st
from backend import generate_tweets

st.set_page_config(page_title="Tweet Generator 🐦", page_icon="🐦", layout="centered")

st.markdown("<h1 style='text-align: center;'>Tweet Generator 🐦</h1>", unsafe_allow_html=True)
st.markdown("🚀 **Generate tweets on any topic**")

topic = st.text_input("Topic", "India")
num_tweets = st.number_input("Number of tweets", min_value=1, max_value=7, value=3)

if st.button("Generate"):
    tweets = generate_tweets(topic, num_tweets)
    for i, tweet in enumerate(tweets, 1):
        st.write(f"{i}. \"{tweet}\"")
