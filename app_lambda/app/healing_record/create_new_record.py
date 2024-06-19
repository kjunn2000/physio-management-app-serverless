import json
import boto3
import uuid
from decimal import Decimal
from datetime import datetime 

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

    event["body"] = {
        "case_id": "C0001",
        "type": "Knee 3 Ligaments",
    }

    event = json.dumps(event)
    
    db_config = DbConfig()

    new_record = generate_new_record(event, db_config)
    
    response = db_config.get_table().put_item(Item=new_record)
    
    print(new_record)

    return {"statusCode": 200, "body": { "record_id" : json.dumps(new_record['RecordId'])}}


def generate_new_record(event, db_config):

    body = json.loads(event)["body"]
    
    body['muscle_size'] = {
        "-10cm(L)": Decimal(str(35)),
        "5cm(L)": Decimal(str(41)),
        "10cm(L)": Decimal(str(44.5)),
        "15cm(L)": Decimal(str(48)),
        "-10cm(R)": Decimal(str(36.5)),
        "5cm(R)": Decimal(str(43)),
        "10cm(R)": Decimal(str(47)),
        "15cm(R)": Decimal(str(51)),
    }

    return {
        "CaseId": body["case_id"],
        "RecordId": generate_record_id(db_config),
        "Type": body["type"],
        "MuscleSize": body["muscle_size"],
        'CreatedDatetime': datetime.now().isoformat()
    }


def generate_record_id(db_config):
    return uuid.uuid4().hex

if __name__ == "__main__":
    main({}, "")
