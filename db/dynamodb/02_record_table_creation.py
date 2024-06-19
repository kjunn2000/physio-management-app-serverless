import boto3

table_name = "RecoveryRecord"
primary_key_attribute_name = "RecoveryRecord"  
sort_key_attribute_name = "AppointmentStartTime"  
# gsi_name = "user-trips-index"

dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:4566")

key_schema = [
    {
        "AttributeName": primary_key_attribute_name,
        "KeyType": "HASH"
    },
    {
        "AttributeName": sort_key_attribute_name,
        "KeyType": "RANGE"  
    }
]

table_attributes = [
    {
        "AttributeName": primary_key_attribute_name,
        "AttributeType": "S"  
    },
    {
        "AttributeName": sort_key_attribute_name,
        "AttributeType": "S"  
    }
]

# Define GSI details
# gsi_key_schema = [
#     {
#         "AttributeName": primary_key_attribute_name,
#         "KeyType": "HASH"
#     }
# ]

# gsi_projection = {
#     "ProjectionType": "ALL"
# }

provisioned_throughput = {
    "ReadCapacityUnits": 5,
    "WriteCapacityUnits": 5
}

# Create the table with GSI
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=table_attributes,
        # GlobalSecondaryIndexes=[
        #     {
        #         "IndexName": gsi_name,
        #         "KeySchema": gsi_key_schema,
        #         "Projection": gsi_projection,
        #         "ProvisionedThroughput": provisioned_throughput
        #     }
        # ],
        ProvisionedThroughput= provisioned_throughput
    )

    print(f"Table '{table_name}' created successfully!")
except Exception as e:
    print(f"Error creating table: {e}")