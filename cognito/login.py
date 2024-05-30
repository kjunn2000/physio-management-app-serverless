import boto3

def login(username, password):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow= 'USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        },
        ClientId='7orfhsu6123jah645i6vbeki1'
    )
    print(response)

if __name__ == '__main__':
    login('kai_admin', 'coxqux-Pyhwir-bogsy1')
