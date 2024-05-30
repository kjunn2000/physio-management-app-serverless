import boto3

def create_user(username, password):
    client = boto3.client('cognito-idp')
    response = client.sign_up(
        ClientId='7orfhsu6123jah645i6vbeki1',
        Username=username,
        Password=password,
    )
    return response

if __name__ == '__main__':
    create_user('kai_admin2', 'TestJun123!')
