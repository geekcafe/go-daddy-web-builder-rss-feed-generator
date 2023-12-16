"""
Image Utiliteis
"""
from io import BytesIO
from urllib.parse import urlparse
from PIL import Image
import requests

from .file_utilities.file_operations import FileOperations
from .aws_utilities.s3_utility import S3Utility


class ImageUtilities:
    """
    Set of utlities
    """

    @staticmethod
    def download_image(url, save_path) -> bool:
        """
        download an image from the web
        """
        success = False
        try:
            # send a GET request to the URL
            response = requests.get(url, stream=True, timeout=15)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Open a local file with write-binary mode
                with open(save_path, 'wb') as file:
                    # Write the content of the response to the file
                    file.write(response.content)
                    success = True
                print(f"Image downloaded successfully to {save_path}")
            else:
                print(f"Failed to download image. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error: {e}")

        return success

    @staticmethod
    def image_exist(url: str) -> bool:
        """
        Check to see if an image exists
        """
        exists = False
        try:
            # Make an HTTP request to the image URL
            response = requests.get(url, timeout=5)
            exists = response.status_code == 200
        finally:
            pass

        return exists

    @staticmethod
    def get_image_info(url: str, feed_s3_bucket: str, cdn_domain: str) -> [str, int, str]:
        """
        Geet the image info from url
        """
        try:
            # Make an HTTP request to the image URL
            response = requests.get(url, timeout=15)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Get image content
            image_content = response.content

            # Open the image using PIL
            image = Image.open(BytesIO(image_content))

            # Get image length and type
            image_length = len(image_content)
            image_type = image.format.lower() if image.format else "jpeg"

            # determine if we need to save the image and store it
            # on our CDN server.
            # todo: pass this in as flag
            feature_on = True
            override_image = True
            if feature_on and not ImageUtilities.has_extension(url):
                try:
                    # save it
                    file_name = f'{ImageUtilities.get_image_name(url)}.{str(image.format).lower()}'
                    key = f'images/{image_length}/{file_name}'

                    if cdn_domain:
                        tmp_url = f"https://{cdn_domain}/{key}"
                        if not ImageUtilities.image_exist(tmp_url) or override_image:
                            print(f'saving image to {tmp_url}')
                            path = '/tmp/images'
                            FileOperations.makedirs(path)
                            path = f'{path}/{file_name}'
                            image.save(path)

                            S3Utility.upload_file_to_s3(feed_s3_bucket, key, path, f"image/{image_type}")

                        url = tmp_url
                    else:
                        print('failed to load cdn name.  images are not being overriden')

                except Exception as e:
                    print(f'failed to save image error: {str(e)}')


            return url, image_length, image_type

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        return url, None, None

    @staticmethod
    def has_extension(url):
        """
        Determine if the url has an extension in it
        """
        file_name = ImageUtilities.get_image_name(url)

        # Check if the last part of the path contains a dot ('.')
        return '.' in file_name


    @staticmethod
    def get_image_name(url):
        """
        Get the image name from the url
        """
        # Parse the URL
        parsed_url = urlparse(url)

        # Get the path component
        path = parsed_url.path

        # return the name
        return path.split('/')[-1]
