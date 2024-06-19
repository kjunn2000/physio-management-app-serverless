
def get_create_table_attributes_with_sort_key(table_name: str, primary_key_attribute_name: str, sort_key_attribute_name: str):
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
    return key_schema, table_attributes

def get_provisioned_througput(read_capacity_unit: int, write_capacity_unit: int):
    provisioned_throughput = {
        "ReadCapacityUnits": read_capacity_unit,
        "WriteCapacityUnits": write_capacity_unit
    }
    return provisioned_throughput