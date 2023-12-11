import feedgenerator
from datetime import datetime
from .html_creator import HtmlCreator
from .page_parser import SiteBuilderPageParser
from .file_utilities.file_operations import FileOperations
from aws_lambda_powertools import Tracer, Logger
logger = Logger()
tracer = Tracer()

# Function to generate the RSS feed
@tracer.capture_method()
def generate_rss_feed(title, link, description, items, author_name = None
                      , include_full_content = True, output="/tmp/feeds/blog-rss-feed.xml"):
    
    
    
    file_name = FileOperations.get_file_from_path(output)
    directory = output.replace(file_name, "")
    # Ensure the directory exists, create it if not
    FileOperations.makedirs(directory)
    FileOperations.clean_directory(directory)
    
    # Create a FeedGenerator object
    feed: feedgenerator.Rss201rev2Feed = feedgenerator.Rss201rev2Feed(
        title=f"{title}",
        link=f"{link}",
        description=f"{description}",
        language="en-us",
        
    )

    logger.info({
        'source': 'generate_rss_feed',
        'link': f'{link}'        
    })

    for item in items:
        blog_link = f'{link}/f/{item["slug"]}'
        # we have a publishedData and a date field.
        publish_date = datetime.fromisoformat(item["publishedDate"][:-1])
        # it's weird that the "date" field seems to be the actual publish date.
        date = datetime.fromisoformat(item["date"][:-1])

        logger.info({
            'source': 'generate_rss_feed',
            'link': f'{blog_link}',
            'include_full_content': f'{include_full_content}'
        })
        content = item["content"]
        if include_full_content:        
            json_data = SiteBuilderPageParser.extract_json_from_webpage(blog_link)
            content_data = SiteBuilderPageParser.get_page_content(json_data)
            content = HtmlCreator.create_html_from_json_content(content_data)
        
        #content = f"<![CDATA[ {content} ]]>"
        image_url = item["featuredImage"]
        image_length, image_type = SiteBuilderPageParser.get_image_info(image_url)
        enclosure: feedgenerator.Enclosure = feedgenerator.Enclosure(image_url, str(image_length), image_type)
        feed.add_item(
            title=item["title"],
            link=blog_link,
            description=content,
            pubdate=date,
            unique_id=item["postId"],
            author_name=author_name,            
            content=content,
            enclosure=enclosure
        )
        

    # Save the feed to an XML file
    
    with open(output, "w", encoding="utf-8") as feed_file:
        feed.write(feed_file, "utf-8")

    #print(f"RSS feed generated and saved to {output}")

    return output

if __name__ == "__main__":
    generate_rss_feed()
