import json

print('loading function')

def lambda_handler(event, context):
    #1parse out query
    
    
    body = json.loads(event['body'])
    print("FirstName:", body["FirstName"])
    print("LastName:", body["LastName"])
    print("Email:", body["Email"])
    print("Contact:", body["Contact"])
    print("Status:", body["Status"])
    print("Address:\n", body["Address"])
    
    #Returne Values
    return {
            'statusCode': 200,
            'isBase64Encoded': False,
            'body': json.dumps("hello"),
            'headers': {
            'content-type': 'application/json',
            "Access-Control-Allow-Methods": 'OPTIONS,GET',
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Header": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        }
    }






