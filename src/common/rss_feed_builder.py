import os
from common.web_page_reader import read_json_from_webpage
from common.rss_feed import generate_rss_feed



def build_rss_feed(url, author, title, site_url, description):
        
    # get the items
    items = read_json_from_webpage(url)
    if items:
        items = items["feed"]
    # generate the feed
    path = generate_rss_feed(title, site_url, description, items, author)

    return path


if __name__ == "__main__":
    # usage 
    url = os.getenv("BLOG_FEED_URL")
    author = os.getenv("BLOG_FEED_AUTHOR")
    title = os.getenv("SITE_TITLE")
    site_url = os.getenv("SITE_URL")
    description = os.getenv("SITE_DESCRIPTION")

    build_rss_feed(url, author, title, site_url, description)