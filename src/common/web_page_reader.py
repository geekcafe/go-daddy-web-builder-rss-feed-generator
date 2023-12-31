import requests
import json
import os

def read_json_from_webpage(url):
    try:
        # Make an HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the JSON content
        json_content = response.json()

        return json_content

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # load a blog feed url from an environment var
    webpage_url = os.getenv("BLOG_FEED_URL")

    # Read JSON content from the web page
    json_data = read_json_from_webpage(webpage_url)

    if json_data:
        # Process and use the JSON data as needed
        print("JSON Data:")
        print(json.dumps(json_data, indent=2))  # Pretty print the JSON data
    else:
        print("Failed to fetch JSON from the web page.")
