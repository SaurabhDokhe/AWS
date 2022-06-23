
import json
import boto3
from boto3.dynamodb.conditions import Attr
from os import environ

poolid = environ["userpoolId"]

#cognito obj
client = boto3.client('cognito-idp')
#dynamo obj
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

print('Loading function')


def lambda_handler(event, context):
    try:
        
        print(type(event["body"]))
        body = json.loads(event["body"])
        
        email=body["Email"]
        userid= body["UserID"]
        new_firstname= body["FirstName"]
        new_lastname= body["LastName"]
        
        response = client.admin_delete_user(
            UserPoolId='us-west-2_z5vwSq93M',
            Username='abcd@hotmail.com'
        )
        
        #Update Attribute
        table.update_item(
            Key={
                'UserID': userid
            },
            UpdateExpression='SET LastName = :val1, FirstName = :val2',
            ExpressionAttributeValues={
            ':val1': new_lastname,
            ':val2': new_firstname
            }
            
        )
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

