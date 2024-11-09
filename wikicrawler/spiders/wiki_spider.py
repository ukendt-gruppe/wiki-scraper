import scrapy
from scrapy.spiders import Spider
from datetime import datetime
import logging
import json
import os

class WikiSpider(Spider):
    name = 'wiki'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_science-fiction_authors']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'LOG_LEVEL': 'DEBUG',
        # Enable job persistence
        'JOBDIR': 'crawls/wiki-science-fiction',
    }

    def __init__(self, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.visited_urls = self.load_visited_urls()

    def load_visited_urls(self):
        """Load previously visited URLs from file"""
        filepath = 'crawls/visited_urls.json'
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return set(json.load(f))
        return set()

    def save_visited_urls(self):
        """Save visited URLs to file"""
        os.makedirs('crawls', exist_ok=True)
        with open('crawls/visited_urls.json', 'w') as f:
            json.dump(list(self.visited_urls), f)

    def closed(self, reason):
        """Called when spider is closed"""
        self.save_visited_urls()
        logging.info(f"Spider closed: {reason}. Visited {len(self.visited_urls)} URLs")

    def parse(self, response):
        # Add current URL to visited set
        self.visited_urls.add(response.url)
        
        # Find all author links in the lists
        author_links = response.css('div.mw-parser-output ul li a[href^="/wiki/"]')
        
        logging.info(f"Found {len(author_links)} author links")
        
        for link in author_links:
            author_name = link.css('::text').get()
            href = link.css('::attr(href)').get()
            full_url = response.urljoin(href)
            
            if (href and 
                not href.startswith('/wiki/Category:') and 
                not href.startswith('/wiki/List_') and 
                full_url not in self.visited_urls):
                
                logging.info(f"Following link to: {author_name} at {full_url}")
                self.visited_urls.add(full_url)
                
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_author_page,
                    meta={'author_name': author_name}
                )

    def parse_author_page(self, response):
        title = response.meta.get('author_name')
        
        # Get paragraphs including both text and link text
        paragraphs = []
        for p in response.css('div#mw-content-text div.mw-parser-output > p:not(.mw-empty-elt)'):
            texts = []
            for element in p.css('::text, a::text').getall():
                if element.strip():
                    texts.append(element.strip())
            paragraphs.append(' '.join(texts))
        
        content = ' '.join(paragraphs)
        
        if title and content:
            logging.info(f"Saving data for: {title}")
            yield {
                'url': response.url,
                'title': title.strip(),
                'content': content.strip(),
                'scraped_at': datetime.utcnow()
            }