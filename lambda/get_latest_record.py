import json
import boto3
from boto3.dynamodb.conditions import Key

class DbConfig:
    def __init__(self):
        self.table_name = "RecoveryRecords"
        self.region_name = "us-east-1"
        self.endpoint_url = "http://localhost:4566"

    def get_table(self):
        dynamodb = boto3.resource(
            "dynamodb", region_name=self.region_name, endpoint_url=self.endpoint_url
        )
        table = dynamodb.Table(self.table_name)
        return table


def main(event, context):

    db_config = DbConfig()
    
    record = get_latest_record(db_config)
    print(record)

def get_latest_record(db_config):
    query_kwargs = {
        'KeyConditionExpression': Key('CaseId').eq('C0001'),
        'ScanIndexForward': False,
        'Limit': 1
    }

    response = db_config.get_table().query(**query_kwargs)
 
    return response["Items"][0]

if __name__ == "__main__":
    main({}, "")