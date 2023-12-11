import requests
import os
from bs4 import BeautifulSoup
import json
from PIL import Image
from io import BytesIO
from .html_creator import HtmlCreator

class SiteBuilderPageParser:
    @staticmethod
    def extract_json_from_webpage(url):
        try:
            # Make an HTTP request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the script containing window._BLOG_DATA
            script_tag = soup.find('script', text=lambda x: '_BLOG_DATA' in x)

            if script_tag:
                # Extract the content of the JavaScript variable
                script_content = script_tag.text
                start_index = script_content.find('{')
                end_index = script_content.rfind('}')
                
                if start_index != -1 and end_index != -1:
                    json_data_str = script_content[start_index:end_index + 1]

                    # Parse the JSON data
                    json_data = json.loads(json_data_str)

                    return json_data
                else:
                    print("Error: No JSON data found in the script tag.")
            else:
                print("Error: Script tag with window._BLOG_DATA not found.")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        return None

    @staticmethod
    def get_page_content(json_data):
        content = None
        temp_content = None
        if "post" in json_data and "fullContent" in json_data["post"]:
            temp_content = json_data["post"]["fullContent"]


       
        if type(temp_content) is str:
            content = json.loads(temp_content)
        else:
            content = temp_content

        return content

    @staticmethod
    def get_image_info(url):
        try:
            # Make an HTTP request to the image URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Get image content
            image_content = response.content

            # Open the image using PIL
            image = Image.open(BytesIO(image_content))

            # Get image length and type
            image_length = len(image_content)
            image_type = image.format.lower() if image.format else None

            return image_length, image_type

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        return None, None

if __name__ == "__main__":
    # Replace 'your_webpage_url' with the actual URL of the web page
    webpage_url = os.getenv("SITE_TEST_BLOG_POST")

    # Extract JSON data from the web page
    json_data = SiteBuilderPageParser.extract_json_from_webpage(webpage_url)
    content_data = SiteBuilderPageParser.get_page_content(json_data)
    content = HtmlCreator.create_html_from_json_content(content_data)
    if content_data:
        # Process and use the JSON data as needed
        print("JSON Data:")
        print(json.dumps(content_data, indent=2))  # Pretty print the JSON data
    else:
        print("Failed to fetch or extract JSON from the web page.")
