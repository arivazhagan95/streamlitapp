import openai
import os
import random
import re

# Configuration for OpenAI-compatible API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-qrstefghuvwxabcdqrstefghuvwxabcdqrstefgh")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # Can be changed to open source API
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def generate_random_tweets(topic: str, num_tweets: int):
    """Generate random topic-related tweets as fallback"""
    
    # Tweet templates with topic placeholders
    templates = [
        f"Just discovered something amazing about {topic}! 🤯 #trending",
        f"Why is everyone talking about {topic}? Let me know your thoughts! 💭",
        f"Hot take: {topic} is going to change everything in 2024 🔥",
        f"Can't stop thinking about {topic} lately... anyone else? 🤔",
        f"Breaking: New developments in {topic} are absolutely mind-blowing! 🚀",
        f"Unpopular opinion: {topic} is underrated and here's why... 🧵",
        f"5 things you didn't know about {topic} that will surprise you! ✨",
        f"The future of {topic} looks incredibly promising! What do you think? 🌟",
        f"Just spent hours researching {topic} and I'm fascinated! 📚",
        f"Quick question: What's your favorite thing about {topic}? Drop it below! 👇",
        f"Today I learned something incredible about {topic}... Thread 🧵",
        f"Reminder: {topic} is more important than you think! Here's why... 💡",
        f"Plot twist: {topic} might be the solution we've been looking for! 🎯",
        f"Anyone else obsessed with {topic} or is it just me? 😅",
        f"The impact of {topic} on our daily lives is underestimated! Thoughts? 💬",
        f"Fun fact about {topic} that will make your day better! 😊",
        f"Why {topic} deserves more attention in 2024 🎪",
        f"Controversial take: {topic} is the most underrated topic right now 🔥",
        f"Just me or is {topic} getting more interesting every day? 📈",
        f"Deep dive into {topic} coming soon... stay tuned! 🎬"
    ]
    
    # Additional topic-specific variations
    action_words = ["exploring", "discovering", "learning about", "diving into", "researching"]
    emotions = ["excited", "curious", "fascinated", "amazed", "intrigued"]
    
    dynamic_templates = [
        f"Currently {random.choice(action_words)} {topic} and feeling {random.choice(emotions)}! 🌟",
        f"The more I learn about {topic}, the more {random.choice(emotions)} I get! 🚀",
        f"Who else is {random.choice(action_words)} {topic} these days? 🤝"
    ]
    
    all_templates = templates + dynamic_templates
    
    # Select random templates and ensure uniqueness
    selected_tweets = random.sample(all_templates, min(num_tweets, len(all_templates)))
    
    # If we need more tweets than templates, generate variations
    while len(selected_tweets) < num_tweets:
        base_template = random.choice(templates)
        # Add some variation to avoid exact duplicates
        emojis = ["🎉", "✨", "🔥", "💫", "🌟", "🚀", "💡", "🎯"]
        variation = base_template + " " + random.choice(emojis)
        if variation not in selected_tweets:
            selected_tweets.append(variation)
    
    return selected_tweets[:num_tweets]

def generate_tweets_with_openai(topic: str, num_tweets: int):
    """Generate tweets using OpenAI API"""
    try:
        client = openai.OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        
        prompt = f"""Generate {num_tweets} creative and engaging tweets about {topic}. 
        Requirements:
        - Each tweet should be unique and interesting
        - Keep tweets under 280 characters
        - Make them engaging and shareable
        - Include relevant emojis where appropriate
        - Return only the tweet text, one per line
        - No numbering or bullet points"""
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.8
        )
        
        tweets_text = response.choices[0].message.content
        
        # Clean and parse tweets
        tweets = []
        for line in tweets_text.split('\n'):
            line = line.strip()
            # Remove numbering, quotes, and bullet points
            line = re.sub(r'^\d+[\.\)]\s*', '', line)
            line = re.sub(r'^[\-\*]\s*', '', line)
            line = line.strip(' "\'')
            
            if line and len(line) > 10:  # Filter out empty or very short lines
                tweets.append(line)
        
        return tweets[:num_tweets]
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        raise e

def generate_tweets(topic: str, num_tweets: int):
    """Main function to generate tweets with fallback to random generation"""
    try:
        # First, try to generate tweets using OpenAI API
        tweets = generate_tweets_with_openai(topic, num_tweets)
        
        # Check if we got enough tweets
        if len(tweets) >= num_tweets:
            return tweets[:num_tweets]
        else:
            # If not enough tweets, supplement with random ones
            remaining = num_tweets - len(tweets)
            random_tweets = generate_random_tweets(topic, remaining)
            return tweets + random_tweets
            
    except Exception as e:
        # If OpenAI API fails (exhausted, network issues, etc.), use random generation
        print(f"Falling back to random tweet generation due to: {e}")
        return generate_random_tweets(topic, num_tweets)
