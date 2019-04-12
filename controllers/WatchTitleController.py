import os
import boto3
import json
import logging
from models.WatchTitle import WatchTitle


class WatchTitleController:
    LAMBDA_FUNC = os.environ.get('LAMBDA_FUNC')

    def __init__(self):
        logging.info('Setting up boto3')
        self.client = boto3.client(
            'lambda',
            region_name=os.environ.get('AWS_REGION'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS')
        )

    def getWatchTitle(self, request):
        logging.info('Retrieving title info')
        payload = """{{
            "action": "GET",
            "data": {{
                "user": "{}",
                "season": "{}"
            }}
        }}
        """.format(request['user'], request['season'])
        res = self.client.invoke(
            FunctionName=self.LAMBDA_FUNC,
            InvocationType='RequestResponse',
            Payload=payload.encode('utf-8')
        )
        res = json.loads(res['Payload'].read())
        if res['statusCode'] != '200':
            logging.warning('Lambda request failed')
            return json.dumps({'result': 'Failed'})
        return res['body']

    def addWatchTitle(self, watchtitle):
        logging.info('Adding title')
        payload = """{{
            "action": "ADD",
            "data": {}
        }}
        """.format(watchtitle.get_json())
        res = self.client.invoke(
            FunctionName=self.LAMBDA_FUNC,
            InvocationType='RequestResponse',
            Payload=payload.encode('utf-8')
        )
        res = json.loads(res['Payload'].read())
        if res['statusCode'] != '200':
            logging.warning('Lambda request failed')
            return json.dumps({'result': 'Failed'})
        return json.dumps({'result': 'Success'})

    def deleteWatchTitle(self, request):
        payload = """{{
            "action": "DELETE",
            "data": {{
                "user": "{}",
                "season": "{}",
                "title": "{}"
            }}
        }}
        """.format(request['user'], request['season'], request['title'])
        res = self.client.invoke(
            FunctionName=self.LAMBDA_FUNC,
            InvocationType='RequestResponse',
            Payload=payload.encode('utf-8')
        )
        res = json.loads(res['Payload'].read())
        if res['statusCode'] != '200':
            logging.warning('Lambda request failed')
            return json.dumps({'result': 'Failed'})
        return json.dumps({'result': 'Success'})

    def updateWatchTitle(self, request):
        attributes, expression = self.build_update_expr(request)
        payload = """{{
            "action": "UPDATE",
            "data": {{
                "user": "{}",
                "title": "{}",
                "expression": "{}",
                "attributes": {}
            }}
        }}
        """.format(request['user'], request['title'],
                   expression, attributes)
        res = self.client.invoke(
            FunctionName=self.LAMBDA_FUNC,
            InvocationType='RequestResponse',
            Payload=payload.encode('utf-8')
        )
        res = json.loads(res['Payload'].read())
        if res['statusCode'] != '200':
            logging.warning('Lambda request failed')
            return json.dumps({'result': 'Lambda request failed'})
        return json.dumps({'result': 'Success'})

    def build_update_expr(self, data):
        SUBEXPRESSIONS = {
            'isShort': 'isShort = :isShort',
            'startDate': 'startDate = :startDate',
            'op': 'op = :op',
            'ed': 'ed = :ed',
            'bd': 'bd = :bd',
            'watchDay': 'watchDay = :watchDay',
            'channel': 'channel = :channel',
            'others': 'others = :others',
            'latestWatched': 'latestWatched = :latestWatched',
            'remarks': 'remarks = :remarks'
        }
        expression = []
        attributes = {}

        if 'isShort' in data and data['isShort']:
            expression.append(SUBEXPRESSIONS['isShort'])
            attributes.update({':isShort': data['isShort']})
        if 'startDate' in data and data['startDate']:
            expression.append(SUBEXPRESSIONS['startDate'])
            attributes.update({':startDate': data['startDate']})
        if 'op' in data and data['op']:
            expression.append(SUBEXPRESSIONS['op'])
            attributes.update({':op': data['op']})
        if 'ed' in data and data['ed']:
            expression.append(SUBEXPRESSIONS['ed'])
            attributes.update({':ed': data['ed']})
        if 'bd' in data and data['bd']:
            expression.append(SUBEXPRESSIONS['bd'])
            attributes.update({':bd': data['bd']})
        if 'watchDay' in data and data['watchDay']:
            expression.append(SUBEXPRESSIONS['watchDay'])
            attributes.update({':watchDay': data['watchDay']})
        if 'channel' in data and data['channel']:
            expression.append(SUBEXPRESSIONS['channel'])
            attributes.update({':channel': data['channel']})
        if 'others' in data and data['others']:
            expression.append(SUBEXPRESSIONS['others'])
            attributes.update({':others': data['others']})
        if 'latestWatched' in data and data['latestWatched']:
            expression.append(SUBEXPRESSIONS['latestWatched'])
            attributes.update({':latestWatched': data['latestWatched']})
        if 'remarks' in data and data['remarks']:
            expression.append(SUBEXPRESSIONS['remarks'])
            attributes.update({':remarks': data['remarks']})
        return json.dumps(attributes), 'set ' + ','.join(expression)
