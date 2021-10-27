import json
from Code.ExtractData import *
from Code.SendMail import send
import boto3


def lambda_handler():
    extract()
    send()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
