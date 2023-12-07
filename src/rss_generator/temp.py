import feedgenerator
from datetime import datetime

# Function to generate the RSS feed
def generate_rss_feed():
    # Create a FeedGenerator object
    feed = feedgenerator.Rss201rev2Feed(
        title="Your Website Title",
        link="http://www.yourwebsite.com",
        description="Your website description",
        language="en-us",
    )

    # Fetch your website content dynamically and populate the feed with items
    # Replace this with your actual logic to fetch and iterate through items
    items = [
        {
            "title": "Item Title 1",
            "link": "http://www.yourwebsite.com/item1",
            "description": "Description of Item 1",
            "pubDate": datetime(2023, 12, 6, 12, 0, 0),
        },
        # Add more items as needed
    ]

    for item in items:
        feed.add_item(
            title=item["title"],
            link=item["link"],
            description=item["description"],
            pubdate=item["pubDate"],
        )

    # Save the feed to an XML file
    feed_path = "rss_feed.xml"
    with open(feed_path, "w", encoding="utf-8") as feed_file:
        feed.write(feed_file, "utf-8")

    print(f"RSS feed generated and saved to {feed_path}")

if __name__ == "__main__":
    generate_rss_feed()
