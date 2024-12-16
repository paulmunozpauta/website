import requests
import json
import time

# Replace with your valid Bearer Token and User ID
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJZVxgEAAAAA6RrP3NK1uo60F3MvGA1dJX%2B6e4U%3Duy8JaarDb03WWemu1YCkupNH6WyMUd02d3GVYvuRifsGmim5RN"
USER_ID = "888471305712021508"  # Replace with your Twitter User ID

# API URL to fetch recent tweets
url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results=5"
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

# Function to check the rate limit
def check_rate_limit(token):
    rate_limit_url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(rate_limit_url, headers=headers)
    remaining = response.headers.get("x-rate-limit-remaining", "Unknown")
    reset_time = response.headers.get("x-rate-limit-reset", time.time())
    print(f"Rate Limit Remaining: {remaining}")
    return int(reset_time)

# Function to fetch tweets with retries and rate limit handling
def fetch_tweets_with_retries():
    retries = 3
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 429:
            reset_time = int(response.headers.get("x-rate-limit-reset", time.time() + 60))
            wait_time = reset_time - int(time.time())
            print(f"Rate limit hit. Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time + 5)  # Add buffer time
            
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
            break
    return None

# Fetch tweets and process them
def main():
    print("Checking rate limit...")
    reset_time = check_rate_limit(BEARER_TOKEN)
    print(f"Rate Limit Reset Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_time))}\n")
    
    print("Fetching tweets...")
    tweets = fetch_tweets_with_retries()
    
    if tweets and "data" in tweets:
        # Take only the first 3 tweets
        cleaned_tweets = {"data": [{"text": tweet["text"]} for tweet in tweets["data"][:3]]}
        with open('x_posts.json', 'w') as file:
            json.dump(cleaned_tweets, file, indent=4)
        print("Tweets successfully saved to x_posts.json")
    else:
        print("Failed to fetch tweets.")

if __name__ == "__main__":
    main()
