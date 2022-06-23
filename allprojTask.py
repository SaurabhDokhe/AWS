import json
from os import environ
import boto3
from boto3.dynamodb.conditions import Key


tablename = environ["tablename"]
tasktablename= environ["tasktablename"]

dynamodb = boto3.resource('dynamodb')
table=dynamodb.Table(tablename)
tasktable= dynamodb.Table(tasktablename)

def lambda_handler(event, context):
    
    response = table.scan()
    item= response["Items"]
    
    for i in item:
        projectname = i['AssignedProj']
        username= i['username']
        
        response1 = tasktable.query(
            KeyConditionExpression= Key('proj_name').eq(projectname)
        )
        item= response1['Items']
        for j in item:
            taskname= (j['assignedtask'])
            
        print("username:",username, ", ProjectName:",projectname, ", Taskname:",taskname)
        
    return {
        'statusCode': 202,
        'isBase64Encoded': False,
        'body' : json.dumps("success"),
        'headers': {
        'content-type': 'application/json',
        "Access-Control-Allow-Methods": 'OPTIONS,GET',
        "Access-Control-Allow-Origin": '*',
        "Access-Control-Allow-Header": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        }
    }