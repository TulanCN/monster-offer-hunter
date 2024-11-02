import requests
import json
import time
import re
from bs4 import BeautifulSoup

# def _parse_newcoder_page(data, skip_words, start_date):
#     """Parse the main page data and filter posts based on keywords and start date."""
#     assert data['success'] == True
#     pattern = re.compile("|".join(skip_words)) if skip_words else None
#     res = []
#     for x in data['data']['records']:
#         x = x['data']
#         dic = {"user": x['userBrief']['nickname']}
        
#         if 'contentData' in x:
#             x = x['contentData'] 
#             dic['url'] = 'https://www.nowcoder.com/discuss/' + str(x['id'])
#         elif 'momentData' in x:
#             x = x['momentData']
#             dic['url'] = 'https://www.nowcoder.com/feed/main/detail/' + str(x.get('uuid', ''))
        
#         dic['title'] = x.get('title', 'No Title')
#         dic['content'] = x.get('content', 'No Content')
#         dic['id'] = x.get('id', None)

#         # Keyword filtering
#         text = str(dic['title']) + str(dic['content'])
#         if skip_words and pattern and pattern.search(text):
#             continue

#         createdTime = x.get('createdAt') or x.get('createTime', 0)
#         dic['createTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(createdTime // 1000))
#         dic['editTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x.get('editTime', createdTime) // 1000))
        
#         # Date filtering
#         if dic['editTime'] < start_date:
#             continue  
        
#         res.append(dic)
        
#     return res

def parse_post_page(url):
    """Fetch post page and extract post details and comments."""
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
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

def get_main_posts(page_number=1, keyword="校招", skip_words=[], start_date='2023'):
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
    response = requests.post(url, headers=headers, data=json.dumps(data))
    main_posts = response.json()['data']['records']

    results = []
    for post in main_posts:
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
            continue
        
        # Extract detailed post content and comments
        post_text, comments = parse_post_page(post_info["url"])
        post_info["post_text"] = post_text
        post_info["comments"] = comments
        
        results.append(post_info)
        time.sleep(1)  # Respectful scraping delay

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

if __name__ == "__main__":
    all_posts = []
    num_pages = 5  # Set the number of pages you want to scrape

    for page_number in range(1, num_pages + 1):
        print(f"Scraping page {page_number}...")
        posts = get_main_posts(page_number=page_number)
        all_posts.extend(posts)
        time.sleep(2)  # Delay between page requests to avoid rate limiting
    
    # Save all scraped data to a file
    save_posts_to_file(all_posts)
    print("Scraping completed. Data saved to posts_with_comments.txt.")
