import boto3
import json

s3handle = boto3.client('s3')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': res,
        'headers': {
            'Content-Type': 'text/html',
        },
    }
    

def lambda_handler(event, context):
    banidataPath = 'posts.json'
    bucket = 'banibucket'
    banidata = s3handle.get_object(Bucket=bucket, Key=banidataPath)['Body'].read()
    baniTemplate = "<html>"
    baniTemplate += "<head><meta charset='utf-8'/></head>"
    baniTemplate += "<body>"
    baniTemplate += "<h1>বাণী চিরন্তনী</h1>"
    json_data = json.loads(banidata)
    for row in json_data["banis"]:
        baniTemplate += f"<b>[{row['index']}]</b> {row['text']}</br>"
    baniTemplate += "</body>"
    baniTemplate += "</html>"
    return respond(err=None, res=baniTemplate)