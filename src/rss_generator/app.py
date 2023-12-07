import os
from web_page_reader import read_json_from_webpage
from rss_feed import generate_rss_feed


if __name__ == "__main__":
    url = os.getenv("BLOG_FEED_URL")
    author = os.getenv("BLOG_FEED_AUTHOR")
    title = os.getenv("SITE_TITLE")
    site_url = os.getenv("SITE_URL")
    description = os.getenv("SITE_DESCRIPTION")
    
    # get the items
    items = read_json_from_webpage(url)
    if items:
        items = items["feed"]
    # generate the feed
    generate_rss_feed(title, site_url, description, items, author)