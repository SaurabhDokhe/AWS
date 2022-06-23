import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('Users')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    print(event)

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        print( response['ContentType'])
        
        response1 = s3.get_object_tagging(
            Bucket= bucket,
            Key= key
            )
        print(response1)
        a= ""
        b= ""
        
        for tag in response1['TagSet']:
            print(tag)
            print('tagkey', tag['Key'])
            print('tagValue', tag['Value'])
            
            if tag['Key']== 'Email':
                a= tag['Value']
                keyy='landing-module5'
                
                response = s3.copy_object(
                Bucket= keyy ,
                CopySource={'Bucket': bucket, 'Key': key},
                Key= key
                ) 
                
                response = s3.delete_object(
                Bucket= bucket ,
                Key= key
                )
                
                table.put_item(
                   Item={
                        'Email' : a
                    }
                )
            
            else:
                print("MoveObj is not eq to Y")
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

