"""
boto3 sessions
"""
import boto3
from aws_lambda_powertools import Logger

logger = Logger(__name__)

class Boto3_Session:
    """
    boto3 session
    """
    def __init__(self, aws_profile = None, aws_region = None):    
        self.aws_profile = aws_profile
        self.aws_region = aws_region
        

    
    @staticmethod
    def get_aws_session(aws_profile: str = None, aws_region: str = None):
        """
        get aws session
        """
        logger.debug({
            "profile": aws_profile,
            "region": aws_region
        })

        boto3_session = None
        try:
            if aws_profile is None and aws_region is None:
                boto3_session = boto3.Session()                
            else:                
                boto3_session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        except Exception as e:
            logger.error(e)


        return  boto3_session
        