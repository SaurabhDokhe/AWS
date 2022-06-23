import json
import os
import boto3
import uuid
id = uuid.uuid1()
from os import environ
import botocore

poolid = environ["userpoolId"]
#cognito
client = boto3.client('cognito-idp')
#dynamodb
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

print('Loading function')


def lambda_handler(event, context):
    try:
        json1_data = json.loads(event["body"])
        print(json1_data)
        email=json1_data["Email"]
        firstname=json1_data["FirstName"]
        lastname=json1_data["LastName"]
        
        print(event)
        
        #create user
        response = client.admin_create_user(
            UserPoolId='us-east-1_UWXOz86wh',
            Username= email,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'custom:FirstName',
                    'Value': firstname
                    
                },
                {
                    'Name': 'custom:LastName',
                    'Value': lastname
                    
                }
                
            ]
        )
        
        #moving items from api to dynamodb
        
        
        #CONN TO EXISTING DB
        
        print(table.item_count)
        
        value = (id.hex)
        
        table.put_item(
            Item={
                'UserID': value,
                'Email': email,
                'FirstName': firstname,
                'LastName': lastname
            }
        )
        print(table.item_count)
        
        msg = "user details updated"
        data = {}
        output = {"Success": True, "Message": msg, "data": data, "error": {}}
        return {
            "statusCode": 200,
            "isBase64Encoded": False,
            "body": json.dumps(output),
            "headers": {
                "content-type": "application/json",
                "Access-Control-Allow-Methods": "OPTIONS,GET",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Header": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            },
        }
    except botocore.exceptions.ClientError as e:
        output = {
            "Success": False,
            "Message": str(e.response["Error"]["Message"]),
            "data": {},
            "error": e.response["Error"]["Code"],
        }
        print("> Exception", output)
        return {
            "statusCode": 202,
            "isBase64Encoded": False,
            "body": json.dumps(output),
            "headers": {
                "content-type": "application/json",
                "Access-Control-Allow-Methods": "OPTIONS,GET",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Header": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            },
        }