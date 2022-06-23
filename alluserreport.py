#importing lib
import json
import boto3
import sys
from os import environ
import reportlab


from boto3.dynamodb.conditions import Key
from reportlab.platypus import SimpleDocTemplate, TableStyle
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.tables import Table
from reportlab.lib.enums import TA_RIGHT,TA_LEFT,TA_CENTER,TA_JUSTIFY
from reportlab.lib.units import inch,cm,mm
from reportlab.lib import colors
#-----------------------------------------


tablename = environ["tablename"]
tasktablename= environ["tasktablename"]

dynamodb = boto3.resource('dynamodb')
table=dynamodb.Table("userproject")
tasktable= dynamodb.Table("ProjectTask")


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
            
        styles = getSampleStyleSheet()
        report = SimpleDocTemplate("/tmp/report.pdf")
        
        elements = []
        row_array = [username, projectname, taskname]
        tableHeading = [row_array]    
        
        R1 = Paragraph("<para align=center> "+ username +"</para>",styles['Normal'])
        R2 = Paragraph("<para align=center> "+ projectname +"</para>",styles['Normal'])
        R3 = Paragraph("<para align=center> "+ taskname +"</para>",styles['Normal'])
            
        row_array = [R1, R2, R3]
        tableRow = [row_array]
        tR=Table(tableRow, [2 * cm, 2 * cm])   
        tR.hAlign = 'LEFT'
        tR.setStyle(TableStyle([("INNERGRID", (0,0), (-1,-1), 0.25, colors.black),("BOX", (0,0), (-1,-1), 0.25, colors.black)]))
        elements.append(tR)
        del tR
        
        elements.append(Spacer(1, 0.3 * cm))
        
        report.build(elements)
        
        
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file('/tmp/report.pdf', 'saurabhd-test', 'Module5report.pdf')
    
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
    
    
    