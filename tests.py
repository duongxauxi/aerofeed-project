import unittest
from unittest.mock import patch, MagicMock
import datetime
from app import app, format_date, extract_image_and_clean_summary

class RSSAppTestCase(unittest.TestCase):
    def setUp(self):
        # Configure Flask application for testing
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_format_date_valid_struct(self):
        # Test valid time struct formatting
        entry = {
            'published_parsed': (2026, 7, 6, 12, 30, 0, 0, 0, 0)
        }
        formatted = format_date(entry)
        self.assertEqual(formatted, 'Jul 06, 2026 12:30 PM')

    def test_format_date_fallback(self):
        # Test fallback to raw string if publication struct is missing
        entry = {
            'published': 'Mon, 06 Jul 2026 12:30:00 GMT'
        }
        formatted = format_date(entry)
        self.assertEqual(formatted, 'Mon, 06 Jul 2026 12:30:00 GMT')

    def test_format_date_missing(self):
        # Test default value if date fields are missing
        entry = {}
        formatted = format_date(entry)
        self.assertEqual(formatted, 'Unknown Date')

    def test_extract_image_and_clean_summary_media_content(self):
        # Test image extraction from media_content field
        entry = {
            'media_content': [{'url': 'https://example.com/img.jpg', 'medium': 'image'}],
            'summary': '<p>Here is some summary content.</p>'
        }
        img_url, summary = extract_image_and_clean_summary(entry)
        self.assertEqual(img_url, 'https://example.com/img.jpg')
        self.assertEqual(summary, 'Here is some summary content.')

    def test_extract_image_and_clean_summary_html_img(self):
        # Test image extraction from <img> tag in HTML summary
        entry = {
            'summary': '<p>Some text. <img src="https://example.com/summary-img.png" /> Other text.</p>'
        }
        img_url, summary = extract_image_and_clean_summary(entry)
        self.assertEqual(img_url, 'https://example.com/summary-img.png')
        self.assertEqual(summary, 'Some text. Other text.')

    def test_extract_image_and_clean_summary_strip_html(self):
        # Test stripping of HTML elements and styling tags
        entry = {
            'summary': '<div><strong>Main Text</strong><script>alert(1)</script><style>body {color: red}</style></div>'
        }
        _, summary = extract_image_and_clean_summary(entry)
        self.assertEqual(summary, 'Main Text')

    def test_index_route(self):
        # Test index page rendering returns HTTP 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AeroFeed', response.data)

    @patch('requests.get')
    def test_api_articles_success(self, mock_get):
        # Mock requests.get response for RSS feed
        mock_response = MagicMock()
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8" ?>
        <rss version="2.0">
        <channel>
            <title>Mock News Feed</title>
            <description>A test description</description>
            <link>https://mocknews.com</link>
            <item>
                <title>Test Article Title</title>
                <link>https://mocknews.com/article1</link>
                <description>This is a test article description.</description>
                <pubDate>Mon, 06 Jul 2026 12:30:00 GMT</pubDate>
            </item>
        </channel>
        </rss>"""
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Call the endpoint
        response = self.client.get('/api/articles?url=https://mocknews.com/rss')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertEqual(data['title'], 'Mock News Feed')
        self.assertEqual(len(data['articles']), 1)
        self.assertEqual(data['articles'][0]['title'], 'Test Article Title')
        self.assertEqual(data['articles'][0]['summary'], 'This is a test article description.')

    def test_api_articles_missing_url(self):
        # Test response when URL parameter is missing
        response = self.client.get('/api/articles?url=')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('Feed URL is required', data['error'])

if __name__ == '__main__':
    unittest.main()
