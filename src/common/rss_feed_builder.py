"""
RSS Feed Builder
"""
from common.web_page_reader import read_json_from_webpage
from common.rss_feed import generate_rss_feed



def build_rss_feed(url: str, author: str, title: str, site_url: str, description: str
                   , s3_bucket: str = None, cdn_domain: str = None):
    """
    Build the RSS Feed
    """
    # get the items
    items = read_json_from_webpage(url)
    if items:
        items = items["feed"]
    # generate the feed
    path = generate_rss_feed(title, site_url, description, items, author, 
                             s3_bucket=s3_bucket, cdn_domain=cdn_domain)

    return path


if __name__ == "__main__":
    # usage
    import os
    _url = os.getenv("BLOG_FEED_URL")
    _author = os.getenv("BLOG_FEED_AUTHOR")
    _title = os.getenv("SITE_TITLE")
    _site_url = os.getenv("SITE_URL")
    _description = os.getenv("SITE_DESCRIPTION")
    _bucket = os.getenv("FEED_S3_BUCKET_NAME")
    _cdn_domain = os.getenv("DOMAIN_NAME")
    build_rss_feed(_url, _author, _title, _site_url, _description, _bucket, _cdn_domain)