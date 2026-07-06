import datetime
import time
from bs4 import BeautifulSoup
import feedparser
from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

# Default RSS Feeds to present as presets
DEFAULT_FEEDS = {
    'techcrunch': 'https://techcrunch.com/feed/',
    'hackernews': 'https://news.ycombinator.com/rss',
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'reddit_news': 'https://www.reddit.com/r/news/.rss'
}

def extract_image_and_clean_summary(entry):
    """
    Extracts an image URL from media_content, enclosures, or summary HTML.
    Cleans all HTML tags from the summary to present a clear text snippet.
    """
    image_url = None
    
    # 1. Look for image in media_content
    media_content = entry.get('media_content')
    if media_content:
        for media in media_content:
            if media.get('medium') == 'image' or media.get('type', '').startswith('image/') or media.get('url'):
                image_url = media.get('url')
                break
                
    # 2. Look for image in enclosures
    enclosures = entry.get('enclosures')
    if not image_url and enclosures:
        for enc in enclosures:
            if enc.get('type', '').startswith('image/') or enc.get('href'):
                image_url = enc.get('href')
                break

    summary_html = entry.get('summary', '') or entry.get('description', '') or ''
    soup = BeautifulSoup(summary_html, 'html.parser')
    
    # 3. Look for first <img> inside summary HTML if none found so far
    if not image_url:
        img_tag = soup.find('img')
        if img_tag and img_tag.get('src'):
            image_url = img_tag.get('src')
            
    # Clean the summary text by removing interactive/styling components and script tags
    for element in soup(['script', 'style', 'iframe', 'button', 'a']):
        element.decompose()
        
    # Get clean text
    summary_text = soup.get_text(separator=' ').strip()
    
    # Trim and clean up whitespace
    summary_text = " ".join(summary_text.split())
    if len(summary_text) > 220:
        summary_text = summary_text[:217] + "..."
        
    return image_url, summary_text

def format_date(entry):
    """
    Format entry publishing date to a user-friendly format: e.g. 'Oct 12, 2023 04:30 PM'.
    """
    struct_time = entry.get('published_parsed') or entry.get('updated_parsed')
    if struct_time:
        try:
            # Struct_time contains 9 elements, we unpack the first 6
            dt = datetime.datetime(*struct_time[:6])
            return dt.strftime("%b %d, %Y %I:%M %p")
        except Exception:
            pass
            
    # Fallback to the raw string if parsing fails
    return entry.get('published') or entry.get('updated') or "Unknown Date"

@app.route('/')
def index():
    return render_template('index.html', default_feeds=DEFAULT_FEEDS)

@app.route('/api/articles')
def get_articles():
    feed_url = request.args.get('url', DEFAULT_FEEDS['techcrunch']).strip()
    
    if not feed_url:
        return jsonify({
            'success': False,
            'error': 'Feed URL is required'
        }), 400

    try:
        # Use requests with a browser agent to bypass potential HTTP 403 blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        response = requests.get(feed_url, headers=headers, timeout=12)
        response.raise_for_status()
        
        # Parse XML content
        feed = feedparser.parse(response.content)
    except requests.exceptions.RequestException as re:
        return jsonify({
            'success': False,
            'error': f'Network request failed: {str(re)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch or parse feed: {str(e)}'
        }), 400

    # feedparser bozo flag indicates malformed XML, but it can still parse it successfully
    if feed.bozo and not feed.entries:
        return jsonify({
            'success': False,
            'error': 'The URL does not point to a valid RSS or Atom feed.'
        }), 400

    articles = []
    # Limit to top 25 articles
    for entry in feed.entries[:25]:
        image_url, clean_summary = extract_image_and_clean_summary(entry)
        
        articles.append({
            'title': entry.get('title', 'No Title'),
            'link': entry.get('link', '#'),
            'published': format_date(entry),
            'summary': clean_summary or 'No preview description available.',
            'image_url': image_url,
            'author': entry.get('author') or feed.feed.get('title', 'RSS Feed Source')
        })

    return jsonify({
        'success': True,
        'title': feed.feed.get('title', 'RSS Feed'),
        'description': feed.feed.get('description', ''),
        'link': feed.feed.get('link', ''),
        'articles': articles
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
