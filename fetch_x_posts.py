import requests
import json
import time

# Replace with your valid Bearer Token and User ID
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJZVxgEAAAAA6RrP3NK1uo60F3MvGA1dJX%2B6e4U%3Duy8JaarDb03WWemu1YCkupNH6WyMUd02d3GVYvuRifsGmim5RN"
USER_ID = "888471305712021508"  # Replace with your Twitter User ID

url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results=3"
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

# Function to fetch tweets with retries
def fetch_tweets_with_retries():
    retries = 3
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limit hit. Waiting for 60 seconds before retrying...")
            time.sleep(60)  # Wait for 1 minute
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
            break
    return None

# Fetch tweets and process
tweets = fetch_tweets_with_retries()
if tweets and "data" in tweets:
    cleaned_tweets = {"data": [{"text": tweet["text"]} for tweet in tweets["data"]]}
    with open('x_posts.json', 'w') as file:
        json.dump(cleaned_tweets, file, indent=4)
    print("Tweets successfully saved to x_posts.json")
else:
    print("Failed to fetch tweets.")
