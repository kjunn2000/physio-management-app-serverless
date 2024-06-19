import json
import boto3

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
    
    record = get_all_records(db_config)
    print(record)

def get_all_records(db_config):
    response = db_config.get_table().scan()
    return response["Items"]

if __name__ == "__main__":
    main({}, "")

