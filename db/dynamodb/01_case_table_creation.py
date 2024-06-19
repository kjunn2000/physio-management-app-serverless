import boto3
from create_table_function import get_create_table_attributes_with_sort_key, get_provisioned_througput 

table_name = "Cases"
primary_key_attribute_name = "InjuryType"  
sort_key_attribute_name = "CaseId"  

dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:4566")

try:
    key_schema, table_attributes = get_create_table_attributes_with_sort_key(table_name, primary_key_attribute_name, 
                                                                             sort_key_attribute_name)
    provisioned_throughput = get_provisioned_througput(5, 5)
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=table_attributes,
        ProvisionedThroughput= provisioned_throughput
    )

    print(f"Table '{table_name}' created successfully!")
except Exception as e:
    print(f"Error creating table: {e}")