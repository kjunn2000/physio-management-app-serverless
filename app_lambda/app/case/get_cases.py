import json

from app_lambda.app.db_config import DbConfig
from boto3.dynamodb.conditions import Key


def handler(event, context):
    injury_type = event['body']['injuryType']

    response = _get_cases_by_injury_type(injury_type)

    return {
        "statusCode": 200,
        "body": response
    }
    
def _get_cases_by_injury_type(injury_type: str):
    table = DbConfig.get_table(table_name= "Cases")
    
    response = table.query(
        KeyConditionExpression=Key('InjuryType').eq(injury_type)
    )

    return response['Items']
