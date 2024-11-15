import requests
import json
import time
import re
from bs4 import BeautifulSoup
import concurrent.futures

def parse_post_page(url):
    """Fetch post page and extract post details and comments."""
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract main post content
        post_text = soup.find("div", class_="feed-content-text")
        post_text = post_text.get_text(strip=True) if post_text else "No post content available"
        
        # Extract comments
        comments = []
        comment_divs = soup.find_all("div", class_="comment-content-box")
        for comment_div in comment_divs:
            comment_text = comment_div.find("span", class_="vue-ellipsis-js-content-text")
            comment_text = comment_text.get_text(strip=True) if comment_text else "No comment text"
            comments.append(comment_text)
        
        return post_text, comments
    except Exception as e:
        print(f"Error parsing post page {url}: {e}")
        return "No post content available", []

def get_main_posts(page_number=1, keyword="秋招", skip_words=[], start_date='2023'):
    """Scrape main page posts and fetch each post's details including comments."""
    url = 'https://gw-c.nowcoder.com/api/sparta/pc/search'
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "application/json"
    }
    data = {
        "type": "all", 
        "query": keyword, 
        "page": page_number, 
        "tag": [], 
        "order": "create"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)
        main_posts = response.json()['data']['records']
    except Exception as e:
        print(f"Error fetching main posts on page {page_number}: {e}")
        return []

    results = []
    
    def process_post(post):
        post_data = post['data']
        post_info = {
            "title": post_data.get('title', 'No title'),
            "content": post_data.get('content', 'No content')
        }
        
        # Determine the correct URL structure
        if 'contentData' in post_data:
            post_info["url"] = f"https://www.nowcoder.com/discuss/{post_data.get('id', '')}"
        elif 'momentData' in post_data and 'uuid' in post_data['momentData']:
            post_info["url"] = f"https://www.nowcoder.com/feed/main/detail/{post_data['momentData']['uuid']}"
        else:
            # Skip this post if both 'id' and 'uuid' are missing
            print("Skipping post due to missing 'id' or 'uuid'")
            return None
        
        # Extract detailed post content and comments
        post_text, comments = parse_post_page(post_info["url"])
        post_info["post_text"] = post_text
        post_info["comments"] = comments
        
        print(f"Keyword [{keyword}] - Fetched post: {post_info['title']}")
        time.sleep(0.1)  # Respectful scraping delay
        return post_info

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_post, post) for post in main_posts]
        for future in concurrent.futures.as_completed(futures):
            post_info = future.result()
            if post_info:
                results.append(post_info)
    
    return results

def save_posts_to_file(posts, filename="posts_with_comments.txt"):
    """Save scraped posts and comments to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        for post in posts:
            f.write(f"Title: {post['title']}\n")
            f.write(f"URL: {post['url']}\n")
            f.write(f"Content: {post['content']}\n")
            f.write(f"Full Post Text: {post['post_text']}\n")
            f.write("Comments:\n")
            for comment in post["comments"]:
                f.write(f" - {comment}\n")
            f.write("\n" + "="*50 + "\n\n")

def get_all_posts(num_pages, keyword):
    all_posts = []
    page_numbers = range(1, num_pages + 1)
    
    def fetch_page(page_number):
        print(f"Scraping page {page_number}, keyword [{keyword}]...")
        posts = get_main_posts(page_number=page_number, keyword=keyword)
        return posts

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_page, page_number) for page_number in page_numbers]
        for future in concurrent.futures.as_completed(futures):
            posts = future.result()
            all_posts.extend(posts)
    
    return all_posts

if __name__ == "__main__":
    num_pages = 10  # Set the number of pages you want to scrape

    keywords = ["秋招", "校招", "面经"]  # List of keywords to search for

    for keyword in keywords:
        all_posts = get_all_posts(num_pages, keyword)
        # Save all scraped data to a file
        save_posts_to_file(all_posts, keyword + ".txt")
        print(f"Scraping completed for keyword '{keyword}'. Data saved to {keyword}.txt.")
