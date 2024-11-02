import requests

def craw_page(page_number):
    url = "https://maimai.cn/sdk/web/content/get_list"
    params = {
        "api": "gossip/v3/square",
        "u": "236329220",
        "page": page_number,
        "before_id": 0
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cookie": "_buuid=m1NB0FikfPCbZENdBDBEu; _buuid.sig=X467EiV-DSegSXHS_j36Oo-GAxI; AGL_USER_ID=04c8b2cb-2c63-42a6-bb42-da344a2caab5; browser_fingerprint=1D8BA63D; guid=GxIZBBsfBBsYHQQbGxNWGxkTGhseGx9WHBkEHRkfBUNYS0xLeQoaBBoEGgQTGBsFT0dFWEJpCgNFQUlPbQpPQUNGCgZmZ35iYQIKHBkEHRkfBV5DYUhPfU9GWlprCgMddR8bdRobCnIKeWUKSUtnCkZPXkRjChFCWUVeRENJS2cCChoEHwVLRkZDUEVn; gdxidpyhxdE=6xzvu8U7IHKA6j6M26JeyGyLnXHGOYLk6EsEKEdy4oI4y%2BrzXlxt9Uv5KALqaYOL2ERJKbS%5Cy3rQN47NVSKAKPeQfHBZzujgDrOon2CDDDzuWyK9gkmv1shaswTgjXOCNs7%5CcrI%5CXjwxtcB3SG%5CEW4cwrDSLU%2BNNRRV5Y4OMJMhjj0%2FW%3A1730089346274; u=236329220; u.sig=D4qKHZQLL_FF-sL7-tkn0UOsd_M; access_token=1.0d0eed95386f8e7162bdce68dfabdb40; access_token.sig=uUmQqjTWZKy09DpgnuMjj368r9Y; u=236329220; u.sig=D4qKHZQLL_FF-sL7-tkn0UOsd_M; access_token=1.0d0eed95386f8e7162bdce68dfabdb40; access_token.sig=uUmQqjTWZKy09DpgnuMjj368r9Y; channel=www; channel.sig=tNJvAmArXf-qy3NgrB7afdGlanM; maimai_version=4.0.0; maimai_version.sig=kbniK4IntVXmJq6Vmvk3iHsSv-Y; HWWAFSESTIME=1730426874129; HWWAFSESID=c93dc11e86c17036e23; csrftoken=Ndb3mhi2-XK3SpM_SnhGPMh5OQWHb-Oszf9A; session=eyJzZWNyZXQiOiJFbktQbUp4OWEtUldnU1pDeUxzUmJEcEMiLCJ1IjoiMjM2MzI5MjIwIiwiX2V4cGlyZSI6MTczMDUxMzI3OTI3NCwiX21heEFnZSI6ODY0MDAwMDB9; session.sig=HuMiGFlirm3vIfI9hfJB2bYUzAs",
        "priority": "u=1, i",
        "referer": "https://maimai.cn/gossip_list",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "x-csrf-token": "Ndb3mhi2-XK3SpM_SnhGPMh5OQWHb-Oszf9A"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Page {page_number} data fetched successfully.")
        
        datas = []
        content_list = data.get("list", [])
        for content in content_list:
            datas.append(content.get("text", ""))
        return datas
    else:
        print(f"Failed to fetch data for page {page_number}: {response.status_code}")
        return []

def save_to_file(filename, all_data):
    with open(filename, "w", encoding="utf-8") as f:
        for page_data in all_data:
            f.write("\n".join(page_data) + "\n")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    all_data = []
    for page_number in range(1, 200):  # Specify the range for pagination
        print(f"Fetching page {page_number}...")
        page_data = craw_page(page_number)
        all_data.append(page_data)
    
    # Save all data to results.txt
    save_to_file("results.txt", all_data)
