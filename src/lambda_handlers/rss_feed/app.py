
import os
import json
from common.rss_feed_builder import build_rss_feed
from common.aws_utilities.s3_utility import S3Utility
from aws_lambda_powertools import Tracer, Logger

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler(capture_response=True)
def lambda_handler(event: dict, context):
    """
    lambda_handler
    """

    logger.info(event)

    if "body" in event:
        data = event["body"]
        if isinstance(data, str):
            data = json.loads(data)
    else:
        data = event
    
    url = get_configuration_value("blog_feed_url", data) 
    author = get_configuration_value("blog_feed_author", data)
    title = get_configuration_value("site_title", data)
    site_url = get_configuration_value("site_url", data)
    description = get_configuration_value("site_description", data)

    feed_s3_bucket = get_configuration_value("feed_s3_bucket_name", data)
    feed_s3_object_key = get_configuration_value("feed_s3_object_key", data, "blog-rss-feed.xml")
    cdn_domain = get_configuration_value("cdn_domain", data)

    output_path = build_rss_feed(url, author, title, site_url, description, feed_s3_bucket, cdn_domain)

    S3Utility.upload_file_to_s3(feed_s3_bucket, feed_s3_object_key, output_path, "text/xml")

    response = {
        'statusCode': 200,
        'body': {
            'message': 'feed generated',
            'local_file': output_path,
            's3_bucket': feed_s3_bucket,
            's3_object_key': feed_s3_object_key
        }
    }

    return response


def get_configuration_value(key: str, payload: dict, default = None):
    value = payload.get(key.lower()) 

    if not value:
        value = os.getenv(key.upper())
    
    if value is None and default is not None:
        value = default

    logger.info({
        'action': 'get_configuration_value',
        'key': f'{key}',
        'value': f'{value}'
    })
    return value