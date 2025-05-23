# News Crawler API

API để crawl tin tức từ VnExpress và VietnamNet.

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install flask flask-cors requests beautifulsoup4
```

2. Chạy API:
```bash
python api.py
```

API sẽ chạy tại địa chỉ: http://localhost:5000

## API Endpoints

### 1. Lấy danh sách danh mục

```
GET /api/categories
```

Query Parameters:
- `source`: Nguồn tin tức ('vnexpress' hoặc 'vietnamnet', mặc định là 'vnexpress')

Ví dụ:
```
GET /api/categories?source=vnexpress
```

Response:
```json
{
    "categories": {
        "thoi-su": 1,
        "the-gioi": 2,
        "kinh-doanh": 3,
        ...
    },
    "category_names": {
        "1": "Thời sự",
        "2": "Thế giới",
        "3": "Kinh doanh",
        ...
    }
}
```

### 2. Lấy tin tức

```
GET /api/news
```

Query Parameters:
- `source`: Nguồn tin tức ('vnexpress' hoặc 'vietnamnet', mặc định là 'vnexpress')
- `category_id`: ID của danh mục (bắt buộc)
- `num_pages`: Số trang muốn crawl (mặc định là 1)
- `num_articles`: Số bài viết muốn lấy chi tiết (mặc định là 10)

Ví dụ:
```
GET /api/news?source=vnexpress&category_id=1&num_pages=2&num_articles=5
```

Response: Mảng các bài viết với định dạng:
```json
[
    {
        "title": "Tiêu đề bài viết",
        "content": "Nội dung đầy đủ của bài viết",
        "excerpt": "Tóm tắt bài viết",
        "image": "URL hình ảnh",
        "category": 1,
        "status": "published"
    },
    ...
]
```

## Lưu ý

- Các file JSON được lưu trong thư mục `news_data`
- API hỗ trợ CORS, có thể gọi từ bất kỳ domain nào
- Mỗi lần gọi API sẽ tạo một file JSON mới với timestamp
- Các danh mục có sẵn:
  - VnExpress: thoi-su, the-gioi, kinh-doanh, giai-tri, the-thao, phap-luat, giao-duc, suc-khoe, doi-song, du-lich, khoa-hoc-cong-nghe, bat-dong-san
  - VietnamNet: thoi-su, the-gioi, kinh-doanh, giai-tri, the-thao, giao-duc, suc-khoe, doi-song, du-lich, cong-nghe, bat-dong-san, oto-xe-may 