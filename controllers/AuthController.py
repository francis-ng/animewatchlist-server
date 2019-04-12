import os
import boto3
import json
from flask import session


class AuthController:
    userpool_id = os.environ.get('AWS_USERPOOL_ID')
    appclient_id = os.environ.get('AWS_APPCLIENT_ID')

    def __init__(self):
        self.client = boto3.client(
            'cognito-idp',
            region_name=os.environ.get('AWS_REGION'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS')
        )

    def register(self, data):
        res = self.client.sign_up(
            ClientId=self.appclient_id,
            Username=data['username'],
            Password=data['password'],
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': data['email']
                }
            ]
        )
        #TODO: handle InvalidPasswordException
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'UserSub' in res:
                return json.dumps({'result': 'Success'})
            else:
                return json.dumps({'result': 'Registration failed'})
        else:
            return res['ResponseMetadata']['HTTPStatusCode']

    def login(self, data):
        res = self.client.initiate_auth(
            ClientId=self.appclient_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': data['username'],
                'PASSWORD': data['password']
            }
        )
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'AuthenticationResult' in res:
                user_auth_data = {
                    'result': 'Authenticated',
                    'token': res['AuthenticationResult']['AccessToken'],
                    'expires_in': res['AuthenticationResult']['ExpiresIn'],
                    'id_token': res['AuthenticationResult']['IdToken'],
                    'refresh_token': res['AuthenticationResult']['RefreshToken'],
                }
                session['username'] = data['username']
                session['token'] = res['AuthenticationResult']['AccessToken']
                session['refresh_token'] = res['AuthenticationResult']['RefreshToken']
                return json.dumps(user_auth_data)
            else:
                return json.dumps({'result': 'Authentication failed'})
        else:
            return res['ResponseMetadata']['HTTPStatusCode']

    def verify(self):
        try:
            res = self.client.get_user(
                AccessToken=session['token']
            )
            if res['ResponseMetadata']['HTTPStatusCode'] == 200:
                return json.dumps(
                    {
                        'result': 'Authenticated',
                        'username': session['username']
                    }
                )
        except self.client.exceptions.NotAuthorizedException:
            res = self.client.initiate_auth(
                ClientId=self.appclient_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'USERNAME': session['username'],
                    'REFRESH_TOKEN': session['refresh_token']
                }
            )
            if res['ResponseMetadata']['HTTPStatusCode'] == 200:
                session['token'] = res['AuthenticationResult']['AccessToken']
                return json.dumps(
                    {
                        'result': 'Authenticated',
                        'username': session['username']
                    }
                )
            else:
                return json.dumps({'result': 'Not logged in'})
