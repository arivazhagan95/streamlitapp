import streamlit as st
from backend import generate_tweets
import os

st.set_page_config(page_title="Tweet Generator 🐦", page_icon="🐦", layout="centered")

st.markdown("<h1 style='text-align: center;'>Tweet Generator 🐦</h1>", unsafe_allow_html=True)
st.markdown("🚀 **Generate tweets on any topic using AI or creative templates**")

# Add configuration section in sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("**API Settings**")
    
    # Show current API configuration
    api_key = os.getenv("OPENAI_API_KEY", "Default key")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    st.text(f"API URL: {base_url}")
    st.text(f"Model: {model}")
    st.text(f"API Key: {'*' * 20 if api_key != 'Default key' else 'Using default'}")
    
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("1. 🤖 Tries AI generation first")
    st.markdown("2. 🎲 Falls back to creative templates if API fails")
    st.markdown("3. ✨ Always generates engaging content!")

# Main interface
topic = st.text_input("Topic", "India", help="Enter any topic you want tweets about")
num_tweets = st.number_input("Number of tweets", min_value=1, max_value=7, value=3, help="Choose how many tweets to generate")

if st.button("Generate Tweets", type="primary"):
    if topic.strip():
        with st.spinner("Generating tweets... 🤖"):
            try:
                tweets = generate_tweets(topic.strip(), num_tweets)
                
                st.success(f"Generated {len(tweets)} tweets about '{topic}'!")
                
                # Display tweets in a nice format
                for i, tweet in enumerate(tweets, 1):
                    with st.container():
                        st.markdown(f"**Tweet {i}:**")
                        st.markdown(f"> {tweet}")
                        st.markdown("---")
                
                # Add copy-to-clipboard functionality
                all_tweets_text = "\n\n".join([f"{i}. {tweet}" for i, tweet in enumerate(tweets, 1)])
                st.text_area("All tweets (copy-friendly format):", all_tweets_text, height=200)
                
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                st.info("💡 The app will automatically use creative templates when AI is unavailable!")
    else:
        st.warning("Please enter a topic to generate tweets about!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🤖 Powered by AI with creative fallback | "
    "🔄 Automatically switches to templates when needed"
    "</div>", 
    unsafe_allow_html=True
)
