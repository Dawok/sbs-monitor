import requests
import json
import time
import os
from bs4 import BeautifulSoup

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Configuration
API_URL = config['API_URL']
DISCORD_WEBHOOK_URL = config['DISCORD_WEBHOOK_URL']
CHECK_INTERVAL = config['CHECK_INTERVAL']
CHECKED_FILE = config['CHECKED_FILE']

# Function to get JSONP data
def get_jsonp(url):
    response = requests.get(url)
    jsonp_text = response.text
    json_str = jsonp_text[jsonp_text.index('(') + 1:jsonp_text.rindex(')')]
    return json.loads(json_str)

# Function to send a message to Discord
def send_discord_webhook(board_no, title, reg_date, thumbnail_url):
    webhook_url = DISCORD_WEBHOOK_URL
    data = {
        "embeds": [{
            "title": title,
            "description": f"A new post is available. [Click here to view](https://programs.sbs.co.kr/enter/gayo/visualboard/54795?cmd=view&page=1&board_no={board_no})",
            "color": 3066993,
            "timestamp": reg_date,
            "thumbnail": {
                "url": thumbnail_url
            }
        }]
    }
    response = requests.post(webhook_url, json=data)
    return response

# Function to extract image URL from CONTENT field
def extract_image_url(content):
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    if img_tag:
        return img_tag['src']
    return None

# Function to load checked board numbers from a file
def load_checked_numbers(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return set(json.load(file))
    return set()

# Function to save checked board numbers to a file
def save_checked_numbers(filename, numbers):
    with open(filename, 'w') as file:
        json.dump(list(numbers), file)

def main():
    print("Starting the script...")
    checked_numbers = load_checked_numbers(CHECKED_FILE)
    print(f"Previously checked board numbers: {checked_numbers}")

    while True:
        try:
            data = get_jsonp(API_URL)
            posts = data['list']
            
            new_posts_detected = False  # Flag to track if new posts are detected

            for post in posts:
                current_number = post['NO']
                title = post['TITLE']
                reg_date = post['REG_DATE']
                content = post['CONTENT']

                if current_number not in checked_numbers:
                    print(f"New post detected with board number: {current_number}")
                    checked_numbers.add(current_number)
                    
                    # Extract thumbnail URL from content
                    thumbnail_url = extract_image_url(content)
                    
                    send_discord_webhook(current_number, title, reg_date, thumbnail_url)
                    save_checked_numbers(CHECKED_FILE, checked_numbers)
                    new_posts_detected = True
            
            if not new_posts_detected:
                print("No new posts detected.")

        except Exception as e:
            print(f'Error: {e}')
        
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
