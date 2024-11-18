from quart import Quart, request
from spiders.niuke.CrawlData import get_all_posts
from cleaner.DefaultCleaner import clean_text

app = Quart(__name__)

@app.route("/api")
async def api():
    return {"hello": "world"}

@app.route('/niuke', methods=['POST'])
async def niuke():
    # 获取请求中的JSON数据
    request_data = await request.get_json()
    company = request_data.get('company')
    job_name = request_data.get('jobName')
    type = request_data.get('type')
    # 把company, job_name, type拼接为关键字
    # 忽略其中的空值
    keyword = ' '.join(filter(None, [company, job_name, type]))

    num_pages = request_data.get('numPages', 1) # 默认值为1
    if num_pages <= 0 or num_pages > 10:
        num_pages = 5
    # 调用爬虫函数获取数据
    all_posts = get_all_posts(num_pages, keyword)
    cleaned_posts = ""
    for post in all_posts:
        post_text = clean_text(post['post_text'])
        if post_text:
            cleaned_posts += post_text
    return {"data" : cleaned_posts}