from flask import Flask, jsonify, request
from flask_cors import CORS
from vn_news_crawler import VnExpressCrawler, VietnamNetCrawler
import json
from datetime import datetime
import os

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize crawlers
vnexpress_crawler = VnExpressCrawler()
vietnamnet_crawler = VietnamNetCrawler()

@app.route('/api/news', methods=['GET'])
def get_news():
    # Get query parameters
    source = request.args.get('source', 'vnexpress')  # Default to vnexpress
    category_id = request.args.get('category_id', type=int)
    num_pages = request.args.get('num_pages', 1, type=int)
    num_articles = request.args.get('num_articles', 10, type=int)
    
    # Validate source
    if source not in ['vnexpress', 'vietnamnet']:
        return jsonify({'error': 'Invalid source. Must be either vnexpress or vietnamnet'}), 400
        
    # Select crawler based on source
    crawler = vnexpress_crawler if source == 'vnexpress' else vietnamnet_crawler
    
    # Find category name from ID
    category_name = None
    for cat_name, cat_id in crawler.categories.items():
        if cat_id == category_id:
            category_name = cat_name
            break
            
    if not category_name:
        return jsonify({'error': f'Invalid category ID for {source}'}), 400
    
    try:
        # Crawl articles
        articles = crawler.crawl_category(category_name, num_pages)
        
        # Get detailed articles
        detailed_articles = crawler.crawl_article_details(articles, num_articles)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source}_{category_name}_{timestamp}.json"
        
        # Create news_data directory if it doesn't exist
        os.makedirs('news_data', exist_ok=True)
        
        # Save to file in news_data directory
        filepath = os.path.join('news_data', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(detailed_articles, f, ensure_ascii=False, indent=4)
            
        # Return just the array of articles
        return jsonify(detailed_articles)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    source = request.args.get('source', 'vnexpress')
    
    if source not in ['vnexpress', 'vietnamnet']:
        return jsonify({'error': 'Invalid source. Must be either vnexpress or vietnamnet'}), 400
        
    crawler = vnexpress_crawler if source == 'vnexpress' else vietnamnet_crawler
    
    categories = {
        'categories': crawler.categories,
        'category_names': crawler.category_names
    }
    
    return jsonify(categories)

if __name__ == '__main__':
    app.run(debug=True) 