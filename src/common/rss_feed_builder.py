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
    url = os.getenv("BLOG_FEED_URL")
    author = os.getenv("BLOG_FEED_AUTHOR")
    title = os.getenv("SITE_TITLE")
    site_url = os.getenv("SITE_URL")
    description = os.getenv("SITE_DESCRIPTION")
    bucket = os.getenv("FEED_S3_BUCKET_NAME")
    cdn_domain = os.getenv("DOMAIN_NAME")
    build_rss_feed(url, author, title, site_url, description, bucket, cdn_domain)