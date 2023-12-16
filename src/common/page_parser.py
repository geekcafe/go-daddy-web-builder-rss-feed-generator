"""
Page Parser
"""
import json
import requests
from bs4 import BeautifulSoup

class SiteBuilderPageParser:
    """
    Site Builder Page Parser: Parses a web page created by GoDaddy WebSite Builder
    """
    @staticmethod
    def extract_json_from_webpage(url):
        """
        Extract json from a web page
        """
        try:
            # Make an HTTP request to the URL
            response = requests.get(url, timeout=15)
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
        """
        Get Page Content from json data
        """
        content = None
        temp_content = None
        if "post" in json_data and "fullContent" in json_data["post"]:
            temp_content = json_data["post"]["fullContent"]

        if isinstance(temp_content, str):
            content = json.loads(temp_content)
        else:
            content = temp_content

        return content
