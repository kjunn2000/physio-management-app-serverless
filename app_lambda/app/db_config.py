import boto3


class DbConfig:
    region_name = "us-east-1"
    endpoint_url = "http://localhost:4566"

    @staticmethod
    def get_table(table_name: str):
        dynamodb = boto3.resource(
            "dynamodb", region_name=DbConfig.region_name, endpoint_url=DbConfig.endpoint_url
        )
        return dynamodb.Table(table_name)
