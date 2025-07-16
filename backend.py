import random

def generate_tweets(topic: str, num_tweets: int):
    templates = [
        f"{topic}'s rich cultural heritage and diverse landscapes make it a truly unique and mesmerizing destination. #Incredible{topic}",
        f"From the bustling streets to the serene backwaters, {topic} offers a sensory overload like no other. #Travel{topic}",
        f"The spirit of unity and resilience in the face of adversity is what makes {topic} truly special. #Proud{topic}",
        f"Discover the flavors, colors, and traditions that make {topic} unforgettable. #Explore{topic}",
        f"Every corner of {topic} tells a story waiting to be heard. #StoryOf{topic}",
        f"Experience the warmth and hospitality that define {topic}. #WelcomeTo{topic}",
        f"Let {topic} surprise you with its wonders and charm. #Amazing{topic}"
    ]
    tweets = random.sample(templates, k=min(num_tweets, len(templates)))
    return tweets
