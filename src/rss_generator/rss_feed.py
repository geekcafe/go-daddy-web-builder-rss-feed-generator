import feedgenerator
from datetime import datetime

# Function to generate the RSS feed
def generate_rss_feed(title, link, description, items, author_name = None):
    # Create a FeedGenerator object
    feed: feedgenerator.Rss201rev2Feed = feedgenerator.Rss201rev2Feed(
        title=f"{title}",
        link=f"{link}",
        description=f"{description}",
        language="en-us",
    )


    for item in items:
        blog_link = f'{link}/f/{item["slug"]}'
        publish_date = datetime.fromisoformat(item["publishedDate"][:-1])
        # date seems to be the actual publish date.
        date = datetime.fromisoformat(item["date"][:-1])
        feed.add_item(
            title=item["title"],
            link=blog_link,
            description=item["title"],
            pubdate=date,
            unique_id=item["postId"],
            author_name=author_name,            
            content=item["content"]
        )

    # Save the feed to an XML file
    feed_path = "rss_feed.xml"
    with open(feed_path, "w", encoding="utf-8") as feed_file:
        feed.write(feed_file, "utf-8")

    print(f"RSS feed generated and saved to {feed_path}")

if __name__ == "__main__":
    generate_rss_feed()
