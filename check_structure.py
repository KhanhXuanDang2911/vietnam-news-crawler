import requests
from bs4 import BeautifulSoup

url = "https://vietnamnet.vn/the-gioi"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Lưu HTML để kiểm tra
with open("vietnamnet_sample.html", "w", encoding="utf-8") as f:
    f.write(response.text[:10000])  # Lưu 10KB đầu tiên để kiểm tra

print("Kiểm tra các cấu trúc phổ biến:")

# Thử các selector cho các container chứa bài viết
container_tests = [
    '.sidebar_1 .box-widget',
    '.list-item',
    '.list_news',
    '.topical-highlight',
    '.vnn-template',
    '.top-story',
    'div.box-item',
    'div.list-item > div',
    'div.clearfix',
    '.list-title',
    'div.TopStory',
    '.item a.link-title'
]

for selector in container_tests:
    items = soup.select(selector)
    print(f"{selector}: {len(items)} phần tử")
    if items and len(items) > 0:
        print(f"  Ví dụ phần tử đầu tiên: {items[0].name} - class: {items[0].get('class')}")
        # Tìm kiếm tiêu đề
        title = items[0].select_one('a')
        if title:
            print(f"  Link đầu tiên: {title.text.strip()[:30]}...")

# Tìm tất cả các link
print("\nKiểm tra các link chính:")
important_links = soup.select('h1 a, h2 a, h3 a, .title a, a.title, a.cms-link, a.link-title')
print(f"Số lượng link quan trọng: {len(important_links)}")
for i, link in enumerate(important_links[:5]):  # Chỉ hiển thị 5 link đầu tiên
    print(f"{i+1}. {link.text.strip()[:50]}... -> {link.get('href')}") 