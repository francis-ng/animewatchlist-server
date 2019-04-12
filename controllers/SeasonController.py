import os
import boto3
import json
import logging


class SeasonController:
    LAMBDA_FUNC = os.environ.get('LAMBDA_FUNC')

    def __init__(self):
        logging.info('Setting up boto3')
        self.client = boto3.client(
            'lambda',
            region_name=os.environ.get('AWS_REGION'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS')
        )

    def getUserSeasons(self, request):
        logging.info('Retrieving user seasons')
        payload = """{{
            "action": "GET SEASONS",
            "data": {{
                "user": "{}"
            }}
        }}
        """.format(request['user'])
        res = self.client.invoke(
            FunctionName=self.LAMBDA_FUNC,
            InvocationType='RequestResponse',
            Payload=payload.encode('utf-8')
        )
        res = json.loads(res['Payload'].read())
        if res['statusCode'] != '200':
            logging.warning('Lambda request failed')
            return False
        return res['body']
