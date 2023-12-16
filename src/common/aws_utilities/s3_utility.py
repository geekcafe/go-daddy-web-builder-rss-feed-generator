"""
s3 utilities
"""
import os
import boto3
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

from common.file_utilities.file_operations import FileOperations
from common.aws_utilities.s3_session import S3Session

logger = Logger(service=__name__)
tracer = Tracer()

s3_session = S3Session()


    
class S3Utility:

    @staticmethod
    @tracer.capture_method
    def download_file(bucket, key, local_directory = None, always_download = False):

        s3_client: boto3.client = s3_session.get_s3_client()
        file_name = S3Utility.get_file_name_from_path(key)
        if local_directory is None:
            local_path = S3Utility.get_local_path_for_file(file_name)
        else:
            local_path = os.path.join(local_directory, file_name)
        

        if not always_download and os.path.exists(local_path):
            return 200, {'path': local_path}
        

        logger.debug({
            'source': 'download_file',
            'action': 'downloading a file from s3',
            'bucket': bucket,
            'key': key,
            'file_name': file_name,
            'local_path': local_path
        })

        
        
        response = None
        error = None
        try:
            # make sure the directories exists
            FileOperations.makedirs(local_directory)

            response = s3_client.download_file(
                bucket,
                key,
                local_path
            )
        except Exception as e:
            error = str(e)
            message = {'metric_filter': 's3_download_error', 'error': str(e)}
            logger.error(message)
            return 500, message
        
        finally:
            file_exists = os.path.exists(local_path)
            logger.debug({
                'source': 'download_file',
                'action': 'downloading a file from s3',
                'bucket': bucket,
                'key': key,
                'file_name': file_name,
                'local_path': local_path,
                'file_exists': file_exists,
                'response': response,
                'errors': error
            })

            if not file_exists:
                message = {
                    'metric_filter': 's3_download_error', 
                    'error': 'file not found in local directory',
                    'bucket': bucket,
                    'key': key,
                    'file_name': file_name,
                    'local_path': local_path,
                }
                raise Exception(message)


        return 200, {'path': local_path}
    

    @staticmethod
    @tracer.capture_method
    def upload_file_to_s3(bucket: str, key: str, local_file_path: str):
        # upload file to s3 bucket
        s3_client: boto3.client = s3_session.get_s3_client()
        
        try:
            
            logger.info({'action': 's3_upload', 'file': local_file_path, 's3_bucket': bucket, 's3_key': key }) 
            response = s3_client.upload_file(local_file_path, bucket, key)
            logger.info({'action': 's3_upload', 'response': response })

        except ClientError as e:
            logger.error({'s3 upload':'failure', 'bucket': bucket, 
                          'key':key, 'local_file_path': local_file_path,
                          'error': str(e)
                        })
            
            raise e
            
        
        s3_path = f"s3://{bucket}/{key}"
        return s3_path

    @staticmethod
    @tracer.capture_method
    def get_local_path_for_file(file_name: str):
        # use /tmp it's the only writeable location for lambda
        local_path = os.path.join("/tmp", file_name)
        return local_path
    

    @staticmethod
    @tracer.capture_method
    def get_file_name_from_path(path: str):
        return path.rsplit('/')[-1]