
from datetime import datetime
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Logger

import boto3

from common.aws_utilities.boto3_session import Boto3_Session
from common.environment_utility import EnvironmentUtility

logger = Logger(service=__name__)
tracer = Tracer()

class S3Session:
    @tracer.capture_method
    def __init__(self, aws_profile = None, aws_region = None) -> None:
        self.aws_profile = aws_profile
        self.aws_region = aws_region
        self.client = None

        if not self.aws_profile:
            self.aws_profile = EnvironmentUtility.AWS_PROFILE

        if not self.aws_region:
            self.aws_profile = EnvironmentUtility.AWS_REGION


    @tracer.capture_method
    def get_s3_client(self, aws_profile = None, aws_region = None):
        """
        Get the S3 Client Object
        """
        if self.client is None or self.aws_profile != aws_profile or self.aws_region != aws_region:
            start=datetime.utcnow()
            logger.debug({'source': 'get_s3_client', 'action': 'create s3 client'
                          , 'aws_profile': f'{aws_profile}', 'aws_region': f'{aws_region}'
                          })

            self.aws_profile = aws_profile
            self.aws_region = aws_region
            session = Boto3_Session.get_aws_session(aws_profile, aws_region)
            config = boto3.session.Config(signature_version='s3v4')
            self.client = session.client('s3', config=config)
            end=datetime.utcnow()
            logger.debug({'source': 'get_s3_client', 'action': 'create s3 client created',
                          'aws_profile': f'{aws_profile}', 'aws_region': f'{aws_region}',
                          'duration': f'{end-start}'                    
                          })

        return self.client
